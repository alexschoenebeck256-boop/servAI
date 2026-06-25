"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Calendar as CalendarIcon, MapPin } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"

interface Job {
  id: string
  status: string
  description: string
  scheduled_at: string
}

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const fetchJobs = async () => {
    try {
      const data = await api.get<Job[]>("/jobs/")
      setJobs(data)
    } catch (err) {
      console.error("Failed to fetch jobs", err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchJobs()
  }, [])

  return (
    <div className="flex flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Jobs</h1>
          <p className="text-muted-foreground">
            Schedule and dispatch your field technicians.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Schedule View</Button>
          <Button>Dispatch Tech</Button>
        </div>
      </div>

      {isLoading ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i}>
              <CardHeader className="pb-2">
                <Skeleton className="h-4 w-[100px] mb-2" />
                <Skeleton className="h-6 w-[150px]" />
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-2/3" />
                  <div className="flex gap-2 mt-4">
                    <Skeleton className="h-8 flex-1" />
                    <Skeleton className="h-8 flex-1" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-12 border-2 border-dashed rounded-lg">
          <p className="text-muted-foreground">No jobs scheduled.</p>
          <Button variant="outline" className="mt-4" onClick={fetchJobs}>Refresh</Button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job) => (
            <Card key={job.id}>
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <Badge variant={job.status === 'COMPLETED' ? 'secondary' : 'default'}>
                    {job.status.replace('_', ' ')}
                  </Badge>
                  <span className="text-xs text-muted-foreground">#{job.id.slice(0, 8)}</span>
                </div>
                <CardTitle className="text-lg mt-1">Service Request</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col gap-2 text-sm">
                  <div className="flex items-center gap-2">
                    <CalendarIcon className="h-4 w-4 text-muted-foreground" />
                    <span>{job.scheduled_at ? new Date(job.scheduled_at).toLocaleString() : 'Not scheduled'}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-muted-foreground" />
                    <span>Technician assigned</span>
                  </div>
                  <p className="mt-2 text-muted-foreground line-clamp-2">
                    {job.description}
                  </p>
                  <div className="mt-4 flex gap-2">
                    <Button variant="outline" size="sm" className="flex-1">Details</Button>
                    <Button size="sm" className="flex-1">Update Status</Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
