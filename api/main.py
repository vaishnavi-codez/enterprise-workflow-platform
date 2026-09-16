from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator
from uuid import uuid4
import time

from monitoring.logger import logger

from agents.workflow import app_workflow
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory

from config.database import SessionLocal, engine
from memory.database_models import Base, User, UserSession

from api.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


# Create database tables if they do not already exist
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Development of Enterprise Workflow Platform with Decision Automation System - Milestone 4"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Memory instances
short_term_memory = ShortTermMemory()
long_term_memory = LongTermMemory()


# -----------------------------
# Request / Response Models
# -----------------------------

class RegisterRequest(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty.")

        if len(value) < 3:
            raise ValueError(
                "Username must contain at least 3 characters."
            )

        if len(value) > 100:
            raise ValueError(
                "Username cannot exceed 100 characters."
            )

        return value


    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:

        if len(value) < 6:
            raise ValueError(
                "Password must contain at least 6 characters."
            )

        return value


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PromptRequest(BaseModel):
    question: str
    session_id: str | None = None

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:

        if not value.strip():
            raise ValueError("Question cannot be empty.")

        return value.strip()


class PromptResponse(BaseModel):
    session_id: str
    response: str


# -----------------------------
# Root
# -----------------------------

@app.get("/")
def root():

    logger.info("Root endpoint accessed")

    return {
        "message": "Multi-Agent AI system is running. Visit /docs to test it."
    }


# -----------------------------
# Register
# -----------------------------

@app.post("/register")
def register(request: RegisterRequest):

    db = SessionLocal()

    try:

        existing_user = db.query(User).filter(
            User.username == request.username
        ).first()

        if existing_user:

            raise HTTPException(
                status_code=400,
                detail="Username already exists."
            )

        new_user = User(
            username=request.username,
            password_hash=hash_password(request.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(
            f"User registered successfully | username={request.username}"
        )

        return {
            "message": "User registered successfully.",
            "username": new_user.username
        }

    finally:

        db.close()


# -----------------------------
# Login
# -----------------------------

@app.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.username == request.username
        ).first()

        if not user or not verify_password(
            request.password,
            user.password_hash
        ):

            logger.warning(
                f"Authentication failed | username={request.username}"
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )

        token = create_access_token(user.username)

        logger.info(
            f"User logged in successfully | username={user.username}"
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:

        db.close()


# -----------------------------
# Protected Ask Endpoint
# -----------------------------

@app.post("/ask", response_model=PromptResponse)
def ask_agent(
    request: PromptRequest,
    current_user: User = Depends(get_current_user)
):

    start_time = time.time()

    db = SessionLocal()

    try:

        # --------------------------------
        # Create or reuse session
        # --------------------------------

        if request.session_id:

            existing_session = db.query(UserSession).filter(
                UserSession.session_id == request.session_id
            ).first()

            if existing_session:

                # Authorization check
                if existing_session.user_id != current_user.id:

                    logger.warning(
                        f"Unauthorized session access | "
                        f"user={current_user.username} | "
                        f"session_id={request.session_id}"
                    )

                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You are not authorized to access this session."
                    )

                session_id = request.session_id

            else:

                # Session ID does not exist.
                # Create it for the current user.

                session_id = request.session_id

                new_session = UserSession(
                    session_id=session_id,
                    user_id=current_user.id
                )

                db.add(new_session)
                db.commit()

        else:

            session_id = str(uuid4())

            new_session = UserSession(
                session_id=session_id,
                user_id=current_user.id
            )

            db.add(new_session)
            db.commit()


        logger.info(
            f"Request received | "
            f"user={current_user.username} | "
            f"session_id={session_id} | "
            f"question={request.question}"
        )


        # --------------------------------
        # Retrieve short-term memory
        # --------------------------------

        conversation_history = short_term_memory.get_history(
            session_id
        )

        logger.info(
            f"Short-term memory retrieved | "
            f"session_id={session_id} | "
            f"messages={len(conversation_history)}"
        )


        # --------------------------------
        # Retrieve long-term memory
        # --------------------------------

        long_term_memories = long_term_memory.get_memories(
            session_id
        )

        logger.info(
            f"Long-term memory retrieved | "
            f"session_id={session_id} | "
            f"memories={len(long_term_memories)}"
        )


        # --------------------------------
        # Store user message
        # --------------------------------

        short_term_memory.add_message(
            session_id,
            "user",
            request.question
        )


        # --------------------------------
        # Shared AgentState
        # --------------------------------

        initial_state = {
            "user_query": request.question,
            "session_id": session_id,
            "conversation_history": conversation_history,
            "long_term_memories": long_term_memories
        }


        # --------------------------------
        # Run Multi-Agent Workflow
        # --------------------------------

        logger.info(
            f"Workflow started | "
            f"session_id={session_id} | "
            f"agents=Planning,Research,Analysis,Decision"
        )

        result = app_workflow.invoke(initial_state)


        logger.info(
            f"Workflow completed | "
            f"session_id={session_id}"
        )


        # --------------------------------
        # Workflow error
        # --------------------------------

        if result.get("error"):

            error_message = result["error"]

            logger.error(
                f"Workflow failed | "
                f"session_id={session_id} | "
                f"error={error_message}"
            )

            short_term_memory.add_message(
                session_id,
                "assistant",
                f"Workflow error: {error_message}"
            )

            raise HTTPException(
                status_code=500,
                detail=error_message
            )


        # --------------------------------
        # Validate final answer
        # --------------------------------

        final_answer = result.get("final_decision")


        if not final_answer or not str(final_answer).strip():

            logger.error(
                f"Decision Agent produced no answer | "
                f"session_id={session_id}"
            )

            raise HTTPException(
                status_code=500,
                detail="Decision Agent did not produce a final answer."
            )


        final_answer = str(final_answer).strip()


        # --------------------------------
        # Store assistant response
        # --------------------------------

        short_term_memory.add_message(
            session_id,
            "assistant",
            final_answer
        )


        # --------------------------------
        # Store long-term memory
        # --------------------------------

        long_term_memory.save_memory(
            session_id,
            final_answer
        )


        # --------------------------------
        # Execution time
        # --------------------------------

        execution_time = time.time() - start_time

        logger.info(
            f"Request completed successfully | "
            f"user={current_user.username} | "
            f"session_id={session_id} | "
            f"duration={execution_time:.2f}s"
        )


        return PromptResponse(
            session_id=session_id,
            response=final_answer
        )


    except HTTPException:

        raise


    except Exception as e:

        execution_time = time.time() - start_time

        logger.exception(
            f"Unexpected workflow error | "
            f"session_id={request.session_id} | "
            f"duration={execution_time:.2f}s | "
            f"error={str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Workflow error: {str(e)}"
        )


    finally:

        db.close()