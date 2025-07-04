import asyncio

from livekit import api 
from livekit.protocol.sip import CreateSIPParticipantRequest, SIPParticipantInfo

async def main():
    livekit_api = api.LiveKitAPI()

    request = CreateSIPParticipantRequest(
        sip_trunk_id = "ST_gkNZHT9mp62U",
        sip_call_to = "+917775099809",
        room_name = "my-sip-room",
        participant_identity = "sip-test",
        participant_name = "Test Caller",
        krisp_enabled = True,
        wait_until_answered = True
    )
    
    try:
        participant = await livekit_api.sip.create_sip_participant(request)
        print(f"Successfully created {participant}")
    except Exception as e:
        print(f"Error creating SIP participant: {e}")
    finally:
        await livekit_api.aclose()

asyncio.run(main())