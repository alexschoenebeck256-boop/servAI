"use client"

import * as React from "react"
import {
  LayoutDashboard,
  Users,
  Briefcase,
  UserSquare2,
  Bot,
  Settings,
  FileText,
  MessageSquare,
} from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"

const data = {
  navMain: [
    {
      title: "Dashboard",
      url: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      title: "Leads",
      url: "/leads",
      icon: Users,
    },
    {
      title: "Jobs",
      url: "/jobs",
      icon: Briefcase,
    },
    {
      title: "Customers",
      url: "/customers",
      icon: UserSquare2,
    },
    {
      title: "Conversations",
      url: "/conversations",
      icon: MessageSquare,
    },
    {
      title: "AI Agents",
      url: "/agents",
      icon: Bot,
    },
    {
      title: "Invoices",
      url: "/invoices",
      icon: FileText,
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings,
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-4 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Bot className="h-5 w-5" />
          </div>
          <span className="text-xl font-bold">ServAI</span>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu>
          {data.navMain.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton asChild tooltip={item.title}>
                <a href={item.url}>
                  <item.icon className="h-4 w-4" />
                  <span>{item.title}</span>
                </a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>
      <SidebarFooter>
        <div className="p-4 text-xs text-muted-foreground">
          &copy; 2024 ServAI Inc.
        </div>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
