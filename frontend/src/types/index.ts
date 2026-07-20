export interface Product {
  id: string
  name: string
  price: number
  shortDescription: string
  thumbnailUrl: string
  category: string
}

export interface ProductDetail extends Product {
  longDescription: string
  reviews: ProductReview[]
}

export interface ProductReview {
  id: string
  author: string
  rating: number
  comment: string
  date: string
}

export interface CartItem {
  product: Product
  quantity: number
}

export interface ProductFilters {
  name?: string
  category?: string
  sort_by?: 'price' | 'name'
  order?: 'asc' | 'desc'
}

export interface ProductListResponse {
  data: Product[]
  total: number
  filters: ProductFilters
}

export type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; message: string }
