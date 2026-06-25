import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"

export default function SettingsPage() {
  return (
    <div className="flex flex-col gap-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Manage your business profile and platform integrations.
        </p>
      </div>

      <Tabs defaultValue="profile" className="space-y-4">
        <TabsList>
          <TabsTrigger value="profile">Business Profile</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="team">Team Members</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Business Information</CardTitle>
              <CardDescription>
                This information will be used by AI agents when communicating with customers.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-2">
                <label className="text-sm font-medium">Business Name</label>
                <Input defaultValue="ServAI Home Services" />
              </div>
              <div className="grid gap-2">
                <label className="text-sm font-medium">Industry</label>
                <Input defaultValue="HVAC & Plumbing" />
              </div>
              <div className="grid gap-2">
                <label className="text-sm font-medium">Support Email</label>
                <Input defaultValue="support@servai-demo.com" />
              </div>
              <Button>Save Changes</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>ServiceTitan</CardTitle>
                <CardDescription>Sync jobs, customers, and pricebook.</CardDescription>
              </CardHeader>
              <CardContent>
                <Badge variant="outline" className="text-green-600 border-green-600 bg-green-50">Connected</Badge>
                <Button variant="outline" className="ml-2">Configure</Button>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>QuickBooks</CardTitle>
                <CardDescription>Sync invoices and payments.</CardDescription>
              </CardHeader>
              <CardContent>
                <Button>Connect Account</Button>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Google LSA</CardTitle>
                <CardDescription>Automate lead capture from Local Services Ads.</CardDescription>
              </CardHeader>
              <CardContent>
                <Badge variant="outline" className="text-green-600 border-green-600 bg-green-50">Connected</Badge>
                <Button variant="outline" className="ml-2">Configure</Button>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Twilio</CardTitle>
                <CardDescription>Power AI voice and SMS conversations.</CardDescription>
              </CardHeader>
              <CardContent>
                <Badge variant="outline" className="text-green-600 border-green-600 bg-green-50">Connected</Badge>
                <Button variant="outline" className="ml-2">Configure</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
