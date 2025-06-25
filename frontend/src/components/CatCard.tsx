'use client';

import { useState } from 'react';
import { Cat } from '@/types/cat';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Pencil, Trash2, DollarSign, Calendar, Award, Eye } from 'lucide-react';
import { EditCatDialog } from './EditCatDialog';
import { DeleteCatDialog } from './DeleteCatDialog';
import { CatDetailsDialog } from './CatDetailsDialog';

interface CatCardProps {
  cat: Cat;
  onUpdate: (updatedCat: Cat) => void;
  onDelete: (catId: number) => void;
}

export function CatCard({ cat, onUpdate, onDelete }: CatCardProps) {
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);

  const formatSalary = (salary: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(salary);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <>
      <Card className="w-full hover:shadow-lg transition-shadow">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl font-bold">{cat.name}</CardTitle>
            <Badge variant="secondary" className="text-sm">
              {cat.breed}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <Award className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">Experience:</span>
              <span className="font-medium">{cat.years_of_experience} years</span>
            </div>
            <div className="flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-muted-foreground" />
              <span className="text-muted-foreground">Salary:</span>
              <span className="font-medium">{formatSalary(cat.salary)}</span>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Calendar className="h-4 w-4" />
            <span>Joined: {formatDate(cat.created_at)}</span>
          </div>

          <div className="flex gap-2 pt-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setIsDetailsOpen(true)}
              className="flex-1"
            >
              <Eye className="h-4 w-4 mr-2" />
              Details
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsEditOpen(true)}
              className="flex-1"
            >
              <Pencil className="h-4 w-4 mr-2" />
              Edit
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onClick={() => setIsDeleteOpen(true)}
              className="flex-1"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Delete
            </Button>
          </div>
        </CardContent>
      </Card>

      <EditCatDialog
        cat={cat}
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        onUpdate={onUpdate}
      />

      <DeleteCatDialog
        cat={cat}
        open={isDeleteOpen}
        onOpenChange={setIsDeleteOpen}
        onDelete={onDelete}
      />

      <CatDetailsDialog
        catId={cat.id}
        open={isDetailsOpen}
        onOpenChange={setIsDetailsOpen}
      />
    </>
  );
}
