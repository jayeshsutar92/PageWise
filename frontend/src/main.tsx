import React from "react";
import ReactDOM from "react-dom/client";
import { AlertCircle, ChevronRight, Loader2, PackageSearch, RotateCcw } from "lucide-react";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const CATEGORIES = ["Books", "Clothing", "Electronics", "Grocery", "Health", "Home", "Outdoors", "Toys"];

type Product = {
  id: number;
  name: string;
  category: string;
  price: string;
  created_at: string;
  updated_at: string;
};

type ProductsResponse = {
  products: Product[];
  next_cursor: string | null;
};

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

function formatPrice(value: string): string {
  return new Intl.NumberFormat(undefined, {
    style: "currency",
    currency: "USD"
  }).format(Number(value));
}

function App() {
  const [category, setCategory] = React.useState("");
  const [products, setProducts] = React.useState<Product[]>([]);
  const [nextCursor, setNextCursor] = React.useState<string | null>(null);
  const [cursorStack, setCursorStack] = React.useState<(string | null)[]>([null]);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const loadProducts = React.useCallback(
    async (cursor: string | null, mode: "replace" | "append") => {
      const params = new URLSearchParams({ limit: "50" });
      if (cursor) params.set("cursor", cursor);
      if (category) params.set("category", category);

      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_URL}/products?${params.toString()}`);
        if (!response.ok) {
          const body = await response.json().catch(() => null);
          throw new Error(body?.detail ?? `Request failed with status ${response.status}`);
        }
        const data = (await response.json()) as ProductsResponse;
        setProducts((current) => (mode === "append" ? [...current, ...data.products] : data.products));
        setNextCursor(data.next_cursor);
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Unable to load products.");
      } finally {
        setIsLoading(false);
      }
    },
    [category]
  );

  React.useEffect(() => {
    setProducts([]);
    setNextCursor(null);
    setCursorStack([null]);
    void loadProducts(null, "replace");
  }, [category, loadProducts]);

  function handleNextPage() {
    if (!nextCursor || isLoading) return;
    setCursorStack((current) => [...current, nextCursor]);
    void loadProducts(nextCursor, "append");
  }

  function handleRefresh() {
    setProducts([]);
    setNextCursor(null);
    setCursorStack([null]);
    void loadProducts(null, "replace");
  }

  return (
    <main className="min-h-screen bg-zinc-50 text-zinc-950">
      <section className="mx-auto flex w-full max-w-6xl flex-col gap-5 px-4 py-6 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-4 border-b border-zinc-200 pb-5 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2 text-sm font-medium text-emerald-700">
              <PackageSearch className="h-4 w-4" aria-hidden="true" />
              Product Browser
            </div>
            <h1 className="text-2xl font-semibold tracking-normal text-zinc-950">Newest products</h1>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <label className="text-sm font-medium text-zinc-700" htmlFor="category">
              Category
            </label>
            <select
              id="category"
              className="h-10 rounded-md border border-zinc-300 bg-white px-3 text-sm shadow-sm outline-none transition focus:border-emerald-600 focus:ring-2 focus:ring-emerald-100"
              value={category}
              onChange={(event) => setCategory(event.target.value)}
            >
              <option value="">All</option>
              {CATEGORIES.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
            <button
              className="inline-flex h-10 items-center gap-2 rounded-md border border-zinc-300 bg-white px-3 text-sm font-medium shadow-sm transition hover:bg-zinc-100 disabled:cursor-not-allowed disabled:opacity-60"
              onClick={handleRefresh}
              disabled={isLoading}
              type="button"
              title="Refresh"
            >
              <RotateCcw className="h-4 w-4" aria-hidden="true" />
              Refresh
            </button>
          </div>
        </header>

        {error ? (
          <div className="flex items-start gap-3 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
            <AlertCircle className="mt-0.5 h-4 w-4 flex-none" aria-hidden="true" />
            <p>{error}</p>
          </div>
        ) : null}

        <div className="overflow-hidden rounded-md border border-zinc-200 bg-white shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] border-collapse text-left text-sm">
              <thead className="bg-zinc-100 text-xs uppercase text-zinc-600">
                <tr>
                  <th className="px-4 py-3 font-semibold">ID</th>
                  <th className="px-4 py-3 font-semibold">Name</th>
                  <th className="px-4 py-3 font-semibold">Category</th>
                  <th className="px-4 py-3 font-semibold">Price</th>
                  <th className="px-4 py-3 font-semibold">Updated</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100">
                {products.map((product) => (
                  <tr key={`${product.updated_at}-${product.id}`} className="hover:bg-zinc-50">
                    <td className="whitespace-nowrap px-4 py-3 font-mono text-xs text-zinc-500">{product.id}</td>
                    <td className="px-4 py-3 font-medium text-zinc-950">{product.name}</td>
                    <td className="px-4 py-3 text-zinc-700">{product.category}</td>
                    <td className="whitespace-nowrap px-4 py-3 text-zinc-700">{formatPrice(product.price)}</td>
                    <td className="whitespace-nowrap px-4 py-3 text-zinc-700">{formatDate(product.updated_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {!isLoading && products.length === 0 ? (
            <div className="px-4 py-12 text-center text-sm text-zinc-600">No products found.</div>
          ) : null}
        </div>

        <div className="flex items-center justify-between gap-3">
          <p className="text-sm text-zinc-600">
            Showing {products.length.toLocaleString()} products
            {cursorStack.length > 1 ? ` across ${cursorStack.length} pages` : ""}
          </p>
          <button
            className="inline-flex h-10 items-center gap-2 rounded-md bg-emerald-700 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:bg-zinc-300"
            onClick={handleNextPage}
            disabled={!nextCursor || isLoading}
            type="button"
          >
            {isLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : null}
            Next page
            <ChevronRight className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

