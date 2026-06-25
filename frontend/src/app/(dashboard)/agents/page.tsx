"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useWebSocket } from "@/hooks/use-websocket"
import { Activity, Play, Square, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"

interface Agent {
  id: string
  agent_type: string
  status: string
  config: any
  efficiency?: string
  tasksCompleted?: number
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [businessId, setBusinessId] = useState<string | null>(null)

  // Get current user to get businessId
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await api.get<any>("/auth/me")
        setBusinessId(user.business_id)
      } catch (err) {
        console.error("Failed to fetch user", err)
      }
    }
    fetchUser()
  }, [])

  const { lastMessage, readyState } = useWebSocket(
    businessId ? `ws://localhost:8000/ws/v1/realtime/${businessId}` : ""
  )

  const fetchAgents = async () => {
    try {
      const data = await api.get<Agent[]>("/agents/")
      setAgents(data)
    } catch (err) {
      console.error("Failed to fetch agents", err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchAgents()
  }, [])

  // Update agents from WebSocket
  useEffect(() => {
    if (lastMessage && lastMessage.type === "agent_status_update") {
      setAgents((prev) =>
        prev.map((a) =>
          a.id === lastMessage.agent_id ? { ...a, status: lastMessage.status } : a
        )
      )
    }
  }, [lastMessage])

  const handleCommand = async (agentId: string, command: string) => {
    try {
      await api.post(`/agents/${agentId}/command`, { command })
      // Refresh agents to see status change if not handled by WS
      fetchAgents()
    } catch (err) {
      console.error("Failed to send command", err)
    }
  }

  return (
    <div className="flex flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Agent Control Panel</h1>
          <p className="text-muted-foreground">
            Monitor and manage your autonomous AI workforce.
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <Activity className={`h-4 w-4 ${readyState === 1 ? 'text-green-500' : 'text-muted-foreground'}`} />
          <span>{readyState === 1 ? 'Live updates active' : 'Offline'}</span>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{agents.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Now</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {agents.filter(a => a.status === "WORKING").length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Efficiency</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">95.4%</div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>AI Workforce</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Agent Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Efficiency</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">
                    Loading agents...
                  </TableCell>
                </TableRow>
              ) : agents.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-center py-8 text-muted-foreground">
                    No agents found.
                  </TableCell>
                </TableRow>
              ) : (
                agents.map((agent) => (
                  <TableRow key={agent.id}>
                    <TableCell className="font-medium">{agent.agent_type}</TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          agent.status === "WORKING"
                            ? "default"
                            : agent.status === "IDLE"
                            ? "secondary"
                            : "outline"
                        }
                      >
                        {agent.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{agent.efficiency || "98%"}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        {agent.status === "IDLE" ? (
                          <Button size="icon" variant="ghost" onClick={() => handleCommand(agent.id, "START")}>
                            <Play className="h-4 w-4" />
                          </Button>
                        ) : (
                          <Button size="icon" variant="ghost" onClick={() => handleCommand(agent.id, "STOP")}>
                            <Square className="h-4 w-4" />
                          </Button>
                        ) }
                        <Button size="icon" variant="ghost">
                          <Settings className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
