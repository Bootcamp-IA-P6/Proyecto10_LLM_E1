import { useQuery } from "@tanstack/react-query";
import { getProfile } from "@/services/api";

export function useActiveProfile() {
  return useQuery({
    queryKey: ["profile"],
    queryFn: getProfile,
    staleTime: 60_000,
  });
}
