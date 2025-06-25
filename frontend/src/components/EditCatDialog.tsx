'use client';

import { useState } from 'react';
import { Cat, CatUpdate } from '@/types/cat';
import { catApi, ApiError } from '@/lib/api';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, DollarSign } from 'lucide-react';

interface EditCatDialogProps {
  cat: Cat;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onUpdate: (updatedCat: Cat) => void;
}

export function EditCatDialog({ cat, open, onOpenChange, onUpdate }: EditCatDialogProps) {
  const [salary, setSalary] = useState(cat.salary.toString());
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const salaryNumber = parseFloat(salary);
      if (isNaN(salaryNumber) || salaryNumber <= 0) {
        throw new Error('Salary must be a positive number');
      }

      const updateData: CatUpdate = { salary: salaryNumber };
      const updatedCat = await catApi.updateCat(cat.id, updateData);

      onUpdate(updatedCat);
      onOpenChange(false);
      setSalary(updatedCat.salary.toString());
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to update cat salary');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenChange = (newOpen: boolean) => {
    if (!isLoading) {
      onOpenChange(newOpen);
      if (!newOpen) {
        setError(null);
        setSalary(cat.salary.toString());
      }
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit {cat.name}&#39;s Salary</DialogTitle>
          <DialogDescription>
            Update the salary for this spy cat. Current salary: ${cat.salary.toLocaleString()}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="salary">New Salary</Label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="salary"
                  type="number"
                  step="0.01"
                  min="0"
                  value={salary}
                  onChange={(e) => setSalary(e.target.value)}
                  className="pl-9"
                  placeholder="Enter new salary"
                  disabled={isLoading}
                  required
                />
              </div>
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => handleOpenChange(false)}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Update Salary
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
