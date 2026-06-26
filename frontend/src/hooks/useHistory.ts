import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { deleteGeneration, getHistory } from "@/services/api";

export function useHistory() {
  return useQuery({
    queryKey: ["history"],
    queryFn: () => getHistory(),
  });
}

export function useDeleteGeneration() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => deleteGeneration(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["history"] }),
  });
}
