import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <div className="flex flex-col gap-2 p-2">
      <h3 className="text-xl font-bold">Welcome.</h3>
    </div>
  );
}
