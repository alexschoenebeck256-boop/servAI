import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Bot } from "lucide-react"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background text-foreground">
      <div className="flex flex-col items-center gap-6 text-center">
        <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
          <Bot className="h-12 w-12" />
        </div>
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl">
            Welcome to ServAI
          </h1>
          <p className="max-w-[600px] text-muted-foreground md:text-xl">
            The autonomous AI operating system for home service businesses.
          </p>
        </div>
        <div className="flex gap-4">
          <Button asChild size="lg">
            <Link href="/dashboard">Open Dashboard</Link>
          </Button>
          <Button variant="outline" size="lg">
            Learn More
          </Button>
        </div>
      </div>
    </div>
  )
}
