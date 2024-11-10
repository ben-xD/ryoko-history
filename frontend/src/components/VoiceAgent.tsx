
import { useConversation } from '@11labs/react';
import { client } from '../clients/httpClient';
import { useState } from 'react';
import {atom, useAtom, useSetAtom} from "jotai"

export const transcriptAtom = atom<any[]>([]);

const MyVoiceAgentComponent = () => {
  const [connected, setConnected] = useState(false);

  const [transcript, setTranscript] = useAtom(transcriptAtom)
  
  const conversation = useConversation({
    onConnect: () => setConnected(true),
    onDisconnect: () => setConnected(false),
    onMessage: (message) => {
      console.log("Message received:", message);
      setTranscript((prevTranscript) => [...prevTranscript, message]); // Append each message to transcript
    },
    onError: (error) => console.error("Error occurred:", error),
    agentId: "agegvPs7GHY2u3z1WD9p"
  });
  
  // Microphone permission handling
  const startConversation = async () => {
    const reply = await client.POST("/conversation/signed-url/");

    const signedURL = reply.data!;

    try {
      await navigator.mediaDevices.getUserMedia({ audio: true });
      const conversationId = await conversation.startSession({
        url: signedURL,
      });
      console.log("Conversation started with ID:", conversationId);
    } catch (error) {
      console.error("Microphone access denied or error:", error);
    }
  };

  const endConversation = async () => {
    await conversation.endSession();
    console.log("Conversation ended.");
  };

  console.log("connected ", connected)
  console.log("transcript ", transcript); 

  return (
    <div>
      <button onClick={startConversation}>Start Conversation</button>
      <button onClick={endConversation}>End Conversation</button>
      {connected && <img style={{paddingTop: "32px",height: "200px",margin: "0 auto",borderRadius: "80px"}} src="/videos/talking.gif" />}
    </div>
  );
};

export default MyVoiceAgentComponent;
