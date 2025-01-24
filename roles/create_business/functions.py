from __future__ import annotations
from dotenv import load_dotenv
load_dotenv(override=True)

import logging
from typing import Annotated

from livekit.agents import (
    JobContext,
    llm,
)
from livekit.api import LiveKitAPI, DeleteRoomRequest


logger = logging.getLogger("")
logger.setLevel(logging.INFO)




class ActorAgentFunctions(llm.FunctionContext):
    def __init__(self, ctx: JobContext):
        self.ctx = ctx
        self.remote_identity = next(iter(ctx.room.remote_participants.values()), None).identity
        super().__init__() 

    def _call_remote(self, method: str, payload: dict):
        try:
            return self.ctx.room.local_participant.perform_rpc(
                destination_identity=self.remote_identity,
                method=method,
                payload=payload
            )
        except Exception as e:
            logger.error(f"Error calling remote method {method}: {e}")
            return None


    @llm.ai_callable()
    async def greet(self):
        """Called as soon as entering in a conversation. This function starts the conversation."""
        try:
            logger.info(f"Greeting user")
            return "Hello! How can I help you today?"
        except Exception as e:
            logger.error(f"Error: {e}")

    @llm.ai_callable()
    async def show_metadata_feedback(
        self,
        business_name: Annotated[str, llm.TypeInfo(description="The name of the business to create.")],
        business_address: Annotated[str, llm.TypeInfo(description="The address of the business.")],
        business_description: Annotated[str, llm.TypeInfo(description="This describes what the business does.")],
    ):
        """
        Called when the assistant feels that it is time to provide a summary of the information collected so far. 
        After the call, the assistant is supposed to acknowlege that the feedback is given. There is no need to
        repeat what information collected, because this function is not going to return anything.
        """
        logger.info(f"Saving idea: {business_name}, {business_address}, {business_description}")
        # return await self._call_remote('save', idea)
    
    @llm.ai_callable()
    async def create_a_business(
        self,
        business_name: Annotated[str, llm.TypeInfo(description="The name of the business to create.")],
        business_address: Annotated[str, llm.TypeInfo(description="The adress of the business.")],
        business_description: Annotated[str, llm.TypeInfo(description="This describes what the business does.")],
    ):
        """
        Called when the assistant is ready to create a new business account after the user has given approval.
        After emits the call, the assistant is supposed to acknowlege that the business is created after it 
        recieves a return value from this function.
        """
        logger.info(f"Going to create business with the following information: {business_name}, {business_address}, {business_description}")
        # TODO: Call the remote function to create a business
        return "ok"
        

    ## Functions that matches the agent.instruct:
    ## 
    # 1. **`start_turn() -> None`**
    # - Initiates the assistant's turn to speak.
    @llm.ai_callable()
    async def start_turn(self):
        """Initiates the assistant's turn to speak."""
        try:
            message = "Starting turn..."
            logger.info(message)
            return message
        except Exception as e:
            logger.error(f"Error: {e}")


    # 2. **`end_turn() -> None`**
    # - Ends the assistant's turn, allowing the user to speak.
    @llm.ai_callable()
    async def end_turn(self):
        """Ends the assistant's turn, allowing the user to speak."""
        try:
            message = "Ending turn..."
            logger.info(message)
            return message
        except Exception as e:
            logger.error(f"Error: {e}")

    # 3. **`wait_for_cue() -> bool`**
    # - Listens for verbal or non-verbal cues indicating it's the assistant's turn to speak.
    @llm.ai_callable()
    async def wait_for_cue(self):
        """Listens for verbal or non-verbal cues indicating it's the assistant's turn to speak."""
        try:
            message = "Waiting for cue..."
            logger.info(message)
            return message
        except Exception as e:
            logger.error(f"Error: {e}")

    # 4. **`provide_cue() -> None`**
    # - Provides a verbal or non-verbal cue to signal the user that it's their turn.
    @llm.ai_callable()
    async def provide_cue(self):
        """Provides a verbal or non-verbal cue to signal the user that it's their turn."""
        try:
            message = "Providing cue..."
            logger.info(message)
            return message
        except Exception as e:
            logger.error(f"Error: {e}")

    # 5. **`process_interruptions() -> None`**
    # - Handles interruptions gracefully, determining if the assistant should yield or continue.
    @llm.ai_callable()
    async def process_interruptions(self):
        """Handles interruptions gracefully, determining if the assistant should yield or continue."""
        try:
            message = "Processing interruptions..."
            logger.info(message)
            return message
        except Exception as e:
            logger.error(f"Error: {e}")
    
    @llm.ai_callable()
    async def terminate_session(self):
        """Called when the conversation should be terminated. This function will end the conversation."""
        try:
            logger.info("🛑 Terminating session...")
            await self._call_remote("terminate", "end_session")
            lkapi = LiveKitAPI()
            await lkapi.room.delete_room(DeleteRoomRequest(
                room=self.ctx.room.name,
                ))
        except Exception as e:
            logger.error(f"Error: {e}")

