import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRef, useState } from "react";
import {
  generateContent,
  generateScience,
  generateNews,
} from "@/services/api";
import type {
  GenerateRequest,
  GenerateResponse,
  ScienceRequest,
  ScienceResponse,
  NewsRequest,
  NewsResponse,
  AnyResult,
} from "@/types/content";

type GenKind = "general" | "science" | "news";

interface UseGenerationOptions {
  kind: GenKind;
}

export function useGeneration({ kind }: UseGenerationOptions) {
  const queryClient = useQueryClient();
  const [result, setResult] = useState<AnyResult | null>(null);
  const lastReq = useRef<GenerateRequest | ScienceRequest | NewsRequest | null>(null);

  const mutation = useMutation({
    mutationFn: async (
      req: GenerateRequest | ScienceRequest | NewsRequest,
    ): Promise<AnyResult> => {
      lastReq.current = req;
      if (kind === "general") return generateContent(req as GenerateRequest) as Promise<GenerateResponse>;
      if (kind === "science") return generateScience(req as ScienceRequest) as Promise<ScienceResponse>;
      return generateNews(req as NewsRequest) as Promise<NewsResponse>;
    },
    onSuccess: (data) => {
      setResult(data);
      queryClient.invalidateQueries({ queryKey: ["history"] });
    },
  });

  const regenerate = () => {
    if (lastReq.current) mutation.mutate(lastReq.current);
  };

  const reset = () => {
    setResult(null);
    mutation.reset();
  };

  return {
    result,
    isLoading: mutation.isPending,
    error: mutation.error ? (mutation.error as Error).message : null,
    submit: mutation.mutate,
    regenerate: lastReq.current ? regenerate : undefined,
    reset,
  };
}
