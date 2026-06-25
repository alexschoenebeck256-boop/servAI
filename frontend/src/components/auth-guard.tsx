"use client"

import { useEffect, useState } from "react"
import { useRouter, usePathname } from "next/navigation"

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()
  const [authorized, setAuthorized] = useState(false)

  useEffect(() => {
    // Check if token exists
    const token = localStorage.getItem("servai_token")
    
    if (!token && pathname !== "/login") {
      setAuthorized(false)
      router.push("/login")
    } else {
      setAuthorized(true)
    }
  }, [pathname, router])

  if (!authorized && pathname !== "/login") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="animate-pulse text-muted-foreground">Loading...</div>
      </div>
    )
  }

  return <>{children}</>
}
