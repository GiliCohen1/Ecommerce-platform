import type { ProductDetail, ProductFilters, ProductListResponse } from '@/types'
import client from './client'

export async function getProducts(filters: ProductFilters = {}): Promise<ProductListResponse> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== ''),
  )
  const { data } = await client.get<ProductListResponse>('/products', { params })
  return data
}

export async function getProductById(id: string): Promise<ProductDetail> {
  const { data } = await client.get<ProductDetail>(`/products/${id}`)
  return data
}
