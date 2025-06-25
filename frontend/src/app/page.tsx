'use client';

import { useState, useEffect } from 'react';
import { Cat } from '@/types/cat';
import { catApi, ApiError } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { Plus, Cat as CatIcon, AlertCircle } from 'lucide-react';
import { CatCard } from '@/components/CatCard';
import { AddCatDialog } from '@/components/AddCatDialog';

export default function Home() {
  const [cats, setCats] = useState<Cat[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);

  const loadCats = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await catApi.getCats();
      setCats(response.cats);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Failed to load spy cats');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCats();
  }, []);

  const handleAddCat = (newCat: Cat) => {
    setCats(prev => [newCat, ...prev]);
  };

  const handleUpdateCat = (updatedCat: Cat) => {
    setCats(prev => prev.map(cat => cat.id === updatedCat.id ? updatedCat : cat));
  };

  const handleDeleteCat = (catId: number) => {
    setCats(prev => prev.filter(cat => cat.id !== catId));
  };

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="space-y-3">
              <Skeleton className="h-[200px] w-full rounded-lg" />
            </div>
          ))}
        </div>
      );
    }

    if (error) {
      return (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            {error}
            <Button
              variant="outline"
              size="sm"
              onClick={loadCats}
              className="ml-4"
            >
              Try Again
            </Button>
          </AlertDescription>
        </Alert>
      );
    }

    if (cats.length === 0) {
      return (
        <div className="text-center py-12">
          <CatIcon className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">No Spy Cats Found</h3>
          <p className="text-muted-foreground mb-4">
            Get started by adding your first spy cat to the agency.
          </p>
          <Button onClick={() => setIsAddDialogOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add First Spy Cat
          </Button>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cats.map((cat) => (
          <CatCard
            key={cat.id}
            cat={cat}
            onUpdate={handleUpdateCat}
            onDelete={handleDeleteCat}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Spy Cat Agency</h1>
          <p className="text-muted-foreground">
            Manage your elite team of spy cats
          </p>
        </div>
        <Button onClick={() => setIsAddDialogOpen(true)} size="lg">
          <Plus className="mr-2 h-4 w-4" />
          Add Spy Cat
        </Button>
      </div>

      {renderContent()}

      <AddCatDialog
        open={isAddDialogOpen}
        onOpenChange={setIsAddDialogOpen}
        onAdd={handleAddCat}
      />
    </div>
  );
}
