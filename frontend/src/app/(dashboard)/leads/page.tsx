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
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Plus, ExternalLink } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"

interface Lead {
  id: string
  customer_id?: string
  status: string
  source: string
  summary: string
  created_at: string
  customer?: {
    first_name: string
    last_name: string
    phone: string
  }
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [search, setSearch] = useState("")

  const fetchLeads = async () => {
    try {
      const data = await api.get<Lead[]>("/leads/")
      setLeads(data)
    } catch (err) {
      console.error("Failed to fetch leads", err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchLeads()
  }, [])

  const filteredLeads = leads.filter(lead => 
    lead.summary?.toLowerCase().includes(search.toLowerCase()) ||
    lead.source?.toLowerCase().includes(search.toLowerCase()) ||
    (lead.customer && `${lead.customer.first_name} ${lead.customer.last_name}`.toLowerCase().includes(search.toLowerCase()))
  )

  return (
    <div className="flex flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Leads</h1>
          <p className="text-muted-foreground">
            Manage and track your incoming business opportunities.
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Lead
        </Button>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search leads..."
            className="pl-8"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <Button variant="outline">Filters</Button>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Customer</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Source</TableHead>
                <TableHead>Summary</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <TableRow key={i}>
                    <TableCell><Skeleton className="h-4 w-[120px]" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-[80px]" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-[100px]" /></TableCell>
                    <TableCell><Skeleton className="h-4 w-[200px]" /></TableCell>
                    <TableCell className="text-right"><Skeleton className="h-8 w-8 ml-auto rounded-full" /></TableCell>
                  </TableRow>
                ))
              ) : filteredLeads.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                    No leads found.
                  </TableCell>
                </TableRow>
              ) : (
                filteredLeads.map((lead) => (
                  <TableRow key={lead.id}>
                    <TableCell className="font-medium">
                      {lead.customer ? `${lead.customer.first_name} ${lead.customer.last_name}` : "Unknown"}
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          lead.status === "NEW"
                            ? "default"
                            : lead.status === "QUALIFYING"
                            ? "secondary"
                            : lead.status === "BOOKED"
                            ? "outline"
                            : "destructive"
                        }
                      >
                        {lead.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{lead.source}</TableCell>
                    <TableCell className="max-w-[300px] truncate">
                      {lead.summary}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="icon">
                        <ExternalLink className="h-4 w-4" />
                      </Button>
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
