"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { useWebSocket } from "@/hooks/use-websocket"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { 
  Users, 
  Briefcase, 
  DollarSign, 
  Bot,
  TrendingUp,
  Activity
} from "lucide-react"

export default function DashboardPage() {
  const [stats, setStats] = useState({
    leads: 0,
    jobs: 0,
    revenue: "$12,450.00",
    agents: 0
  })
  const [activities, setActivities] = useState([
    { time: "2m ago", text: "Sales Agent qualified a lead for HVAC repair", icon: Users },
    { time: "15m ago", text: "Finance Agent issued Invoice #INV-004", icon: DollarSign },
    { time: "1h ago", text: "Ops Agent dispatched Mike to AC Maintenance job", icon: Briefcase },
    { time: "3h ago", text: "Marketing Agent adjusted Google Ads budget", icon: TrendingUp },
  ])
  const [businessId, setBusinessId] = useState<string | null>(null)

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const user = await api.get<any>("/auth/me")
        setBusinessId(user.business_id)
        
        const agents = await api.get<any[]>("/agents/")
        const leads = await api.get<any[]>("/leads/")
        setStats(prev => ({
          ...prev,
          agents: agents.length,
          leads: leads.length
        }))
      } catch (err) {
        console.error("Failed to fetch dashboard stats", err)
      }
    }
    fetchInitialData()
  }, [])

  const { lastMessage, readyState } = useWebSocket(
    businessId ? `ws://localhost:8000/ws/v1/realtime/${businessId}` : ""
  )

  useEffect(() => {
    if (lastMessage) {
      if (lastMessage.type === "new_lead") {
        setStats(prev => ({ ...prev, leads: prev.leads + 1 }))
        setActivities(prev => [
          { time: "Just now", text: `New lead from ${lastMessage.source || 'Web'}`, icon: Users },
          ...prev.slice(0, 3)
        ])
      } else if (lastMessage.type === "agent_action") {
        setActivities(prev => [
          { time: "Just now", text: lastMessage.description, icon: Bot },
          ...prev.slice(0, 3)
        ])
      }
    }
  }, [lastMessage])

  return (
    <div className="flex flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Overview</h1>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Activity className="h-4 w-4 text-green-500" />
          <span>System autonomous and healthy</span>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">New Leads Today</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.leads}</div>
            <p className="text-xs text-muted-foreground">+20% from yesterday</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Jobs Scheduled</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">4 in progress</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue MTD</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.revenue}</div>
            <p className="text-xs text-muted-foreground">+12.5% from last month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Agent Uptime</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">99.9%</div>
            <p className="text-xs text-muted-foreground">{stats.agents} agents online</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { time: "2m ago", text: "Sales Agent qualified a lead for HVAC repair", icon: Users },
                { time: "15m ago", text: "Finance Agent issued Invoice #INV-004", icon: DollarSign },
                { time: "1h ago", text: "Ops Agent dispatched Mike to AC Maintenance job", icon: Briefcase },
                { time: "3h ago", text: "Marketing Agent adjusted Google Ads budget", icon: TrendingUp },
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-4 text-sm">
                  <div className="mt-1 rounded-full bg-muted p-1">
                    <item.icon className="h-3 w-3" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <p>{item.text}</p>
                    <p className="text-xs text-muted-foreground">{item.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Agent Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="rounded-lg border bg-muted/50 p-4">
                <p className="text-sm font-semibold">CEO Agent Recommendation</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  &quot;Marketing spend on Google Ads is yielding 4x ROAS. I recommend increasing the daily budget by 15% for the next week.&quot;
                </p>
                <div className="mt-4 flex gap-2">
                  <Button variant="link" size="sm" className="h-auto p-0">Approve Adjustment</Button>
                  <Button variant="link" size="sm" className="h-auto p-0 text-muted-foreground">Dismiss</Button>
                </div>
              </div>
              <div className="rounded-lg border bg-muted/50 p-4">
                <p className="text-sm font-semibold">CS Agent Alert</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  &quot;High volume of queries regarding electrical panel upgrades. I&apos;ve updated the Knowledge Base with the new pricing tier.&quot;
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
