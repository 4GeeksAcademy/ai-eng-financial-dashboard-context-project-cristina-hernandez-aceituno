import { lazy, Suspense } from 'react'
import { Skeleton } from '@/components/ui/skeleton'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import type { MonthlyDataPoint } from '@/lib/financial-types'

const IncomeOutcomeChartComponent = lazy(() =>
  import('./income-outcome-chart').then((m) => ({
    default: m.IncomeOutcomeChart,
  }))
)

interface IncomeOutcomeChartLazyProps {
  data: MonthlyDataPoint[]
  loading?: boolean
}

function ChartSkeleton() {
  return (
    <Card className="border-border/60">
      <CardHeader className="pb-4">
        <Skeleton className="h-5 w-52" />
        <Skeleton className="h-3 w-64 mt-1" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-[280px] w-full rounded-lg" />
      </CardContent>
    </Card>
  )
}

export function IncomeOutcomeChartLazy({ data, loading }: IncomeOutcomeChartLazyProps) {
  if (loading) {
    return <ChartSkeleton />
  }

  return (
    <Suspense fallback={<ChartSkeleton />}>
      <IncomeOutcomeChartComponent data={data} loading={loading} />
    </Suspense>
  )
}
