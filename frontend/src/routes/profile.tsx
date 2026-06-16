import { createFileRoute } from "@tanstack/react-router";
import ProfileForm from "@/components/profile/ProfileForm";
import PageHeader from "@/components/shared/PageHeader";

export const Route = createFileRoute("/profile")({
  head: () => ({
    meta: [
      { title: "Perfil de empresa · Digital Content AI" },
      {
        name: "description",
        content: "Configura tu perfil de empresa para personalizar las generaciones.",
      },
    ],
  }),
  component: ProfilePage,
});

function ProfilePage() {
  return (
    <div className="flex flex-col items-center px-4 py-12 gap-8">
      <PageHeader
        eyebrow="Perfil"
        title="Perfil de empresa"
        description="Se aplicará a todas las generaciones."
      />
      <div className="relative w-full max-w-xl bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8 shadow-2xl shadow-black/30">
        <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-emerald-400/50 to-transparent" />
        <ProfileForm />
      </div>
    </div>
  );
}
