export interface Cat {
  id: number;
  name: string;
  years_of_experience: number;
  breed: string;
  salary: number;
  created_at: string;
  updated_at: string;
}

export interface CatCreate {
  name: string;
  years_of_experience: number;
  breed: string;
  salary: number;
}

export interface CatUpdate {
  salary: number;
}

export interface CatListResponse {
  cats: Cat[];
  total: number;
}
