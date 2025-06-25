'use client';

import { useState } from 'react';
import { Cat, CatCreate } from '@/types/cat';
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
import { Loader2, User, Award, Cat as CatIcon, DollarSign } from 'lucide-react';

interface AddCatDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onAdd: (newCat: Cat) => void;
}

export function AddCatDialog({ open, onOpenChange, onAdd }: AddCatDialogProps) {
  const [formData, setFormData] = useState<CatCreate>({
    name: '',
    years_of_experience: 0,
    breed: '',
    salary: 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      if (!formData.name.trim()) {
        throw new Error('Name is required');
      }
      if (!formData.breed.trim()) {
        throw new Error('Breed is required');
      }
      if (formData.years_of_experience < 0) {
        throw new Error('Years of experience cannot be negative');
      }
      if (formData.salary <= 0) {
        throw new Error('Salary must be greater than 0');
      }

      const standardizedData = {
        ...formData,
        breed: formData.breed.charAt(0).toUpperCase() + formData.breed.slice(1).toLowerCase()
      };

      const newCat = await catApi.createCat(standardizedData);
      onAdd(newCat);
      onOpenChange(false);
      resetForm();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to create cat');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      years_of_experience: 0,
      breed: '',
      salary: 0,
    });
    setError(null);
  };

  const handleOpenChange = (newOpen: boolean) => {
    if (!isLoading) {
      onOpenChange(newOpen);
      if (!newOpen) {
        resetForm();
      }
    }
  };

  const handleInputChange = (field: keyof CatCreate, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Spy Cat</DialogTitle>
          <DialogDescription>
            Register a new spy cat to the agency. All fields are required.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="name">Name</Label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="pl-9"
                  placeholder="Enter cat's name"
                  disabled={isLoading}
                  required
                />
              </div>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="breed">Breed</Label>
              <div className="relative">
                <CatIcon className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="breed"
                  value={formData.breed}
                  onChange={(e) => handleInputChange('breed', e.target.value)}
                  className="pl-9"
                  placeholder="Enter cat's breed"
                  disabled={isLoading}
                  required
                />
              </div>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="experience">Years of Experience</Label>
              <div className="relative">
                <Award className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="experience"
                  type="number"
                  min="0"
                  value={formData.years_of_experience}
                  onChange={(e) => handleInputChange('years_of_experience', parseInt(e.target.value) || 0)}
                  className="pl-9"
                  placeholder="Years of spy experience"
                  disabled={isLoading}
                  required
                />
              </div>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="salary">Salary</Label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="salary"
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.salary}
                  onChange={(e) => handleInputChange('salary', parseFloat(e.target.value) || 0)}
                  className="pl-9"
                  placeholder="Annual salary"
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
              Add Spy Cat
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
