import { createLazyFileRoute } from "@tanstack/react-router";
import VacationForm from "../components/VacationForm"

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <VacationForm />
  );
}
