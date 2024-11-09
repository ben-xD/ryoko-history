import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/example")({
  component: () => <div>Hello /example!</div>,
});
