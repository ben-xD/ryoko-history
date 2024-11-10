import { createLazyFileRoute } from "@tanstack/react-router";
import VacationForm from "../components/VacationForm"
import MyVoiceAgentComponent from "../components/VoiceAgent";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <>
    <h2 style={{color: 'white'}} className="text-2xl font-semibold text-gray-800 mt-4">Ryoko Travel Assistant</h2>
    <MyVoiceAgentComponent />
    <VacationForm />
    </>
  );
}
