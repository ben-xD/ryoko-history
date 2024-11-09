import { env } from "@/env";
import { createRootRoute, Outlet } from "@tanstack/react-router";
import React, { Suspense } from "react";

const TanStackRouterDevtools =
  import.meta.env.PROD || !env.enableRouterDevtools
    ? () => null // Render nothing in production
    : React.lazy(() =>
        // Lazy load in development
        import("@tanstack/router-devtools").then((res) => ({
          default: res.TanStackRouterDevtools,
        })),
      );

export const Route = createRootRoute({
  component: () => {
    // const router = useRouterState();

    return (
      <>
        <Outlet />

        <Suspense>
          <TanStackRouterDevtools position={"bottom-right"} />
        </Suspense>
      </>
    );
  },
});
