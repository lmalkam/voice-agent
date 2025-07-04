import os
import json
from dotenv import load_dotenv

from livekit import agents, api
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_KEY = os.getenv("DEEPGRAM_API_KEY")
CARTESIA_KEY = os.getenv("CARTESIA_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
SIP_TRUNK_ID = os.getenv("SIP_TRUNK_ID")  # Set this in your .env

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    # Check for outbound call metadata
    phone_number = None
    if ctx.job.metadata:
        try:
            dial_info = json.loads(ctx.job.metadata)
            phone_number = dial_info.get("phone_number")
        except Exception:
            phone_number = None

    # If a phone number is provided, place an outbound call
    if phone_number:
        sip_participant_identity = phone_number
        try:
            await ctx.api.sip.create_sip_participant(api.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id=SIP_TRUNK_ID,  # Set this in your .env or hardcode
                sip_call_to=phone_number,
                participant_identity=sip_participant_identity,
                wait_until_answered=True,
            ))
            print("Call picked up successfully!")
        except api.TwirpError as e:
            print(f"Error creating SIP participant: {e.message}, "
                  f"SIP status: {e.metadata.get('sip_status_code')} "
                  f"{e.metadata.get('sip_status')}")
            await ctx.shutdown()
            return

    # Set up the agent session as usual
    # session = AgentSession(
    #     stt=deepgram.STT(model="nova-3", language="multi", api_key=DEEPGRAM_KEY),
    #     llm=google.LLM(model="gemini-2.0-flash-exp", api_key=GEMINI_KEY),
    #     ##llm=google.LLM(model="gemini-1.5-pro", api_key=GEMINI_KEY),
    #     tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02", api_key=CARTESIA_KEY),
    #     vad=silero.VAD.load(),
    #     turn_detection=MultilingualModel(),
    # )

    session = AgentSession(
    llm=google.beta.realtime.RealtimeModel(
        model="gemini-2.0-flash-exp",
        voice="Puck",
        temperature=0.8,
        instructions="You are a helpful assistant",
        api_key=GEMINI_KEY,
    )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Only greet the user first if this is NOT an outbound call
    if not phone_number:
        await session.generate_reply(
            instructions="Greet the user and offer your assistance."
        )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint,
                       agent_name="agentic"))
