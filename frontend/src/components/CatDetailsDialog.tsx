'use client';

import { useState, useEffect, useCallback } from 'react';
import { Cat } from '@/types/cat';
import { catApi, ApiError } from '@/lib/api';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { DollarSign, Calendar, Award, User, AlertCircle } from 'lucide-react';

interface CatDetailsDialogProps {
  catId: number | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CatDetailsDialog({ catId, open, onOpenChange }: CatDetailsDialogProps) {
  const [cat, setCat] = useState<Cat | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadCatDetails = useCallback(async () => {
    if (!catId) return;

    try {
      setIsLoading(true);
      setError(null);
      const catData = await catApi.getCat(catId);
      setCat(catData);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load cat details');
      }
    } finally {
      setIsLoading(false);
    }
  }, [catId]);

  useEffect(() => {
    if (open && catId) {
      loadCatDetails();
    }
  }, [open, catId, loadCatDetails]);

  const formatSalary = (salary: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(salary);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleOpenChange = (newOpen: boolean) => {
    onOpenChange(newOpen);
    if (!newOpen) {
      setCat(null);
      setError(null);
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Spy Cat Details</DialogTitle>
          <DialogDescription>
            Detailed information about the spy cat
          </DialogDescription>
        </DialogHeader>

        {isLoading && (
          <div className="space-y-4">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
          </div>
        )}

        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {cat && !isLoading && (
          <div className="space-y-6">
            {/* Header with name and breed */}
            <div className="flex items-center justify-between">
              <h3 className="text-2xl font-bold">{cat.name}</h3>
              <Badge variant="secondary" className="text-lg px-3 py-1">
                {cat.breed}
              </Badge>
            </div>

            {/* Details grid */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <User className="h-4 w-4" />
                  <span>Agent ID</span>
                </div>
                <p className="font-medium">#{cat.id.toString().padStart(4, '0')}</p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Award className="h-4 w-4" />
                  <span>Experience</span>
                </div>
                <p className="font-medium">{cat.years_of_experience} years</p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <DollarSign className="h-4 w-4" />
                  <span>Annual Salary</span>
                </div>
                <p className="font-medium text-lg">{formatSalary(cat.salary)}</p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span>Status</span>
                </div>
                <Badge variant="outline" className="w-fit">
                  Active Agent
                </Badge>
              </div>
            </div>

            {/* Timestamps */}
            <div className="border-t pt-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Recruited:</span>
                <span>{formatDate(cat.created_at)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Last Updated:</span>
                <span>{formatDate(cat.updated_at)}</span>
              </div>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
