import { LogOut } from 'lucide-react';

export default function UserProfile({ user, onLogout }) {
  if (!user || user.type === 'GUEST') return null;

  // Extract initial for avatar
  const initial = user.name ? user.name.charAt(0).toUpperCase() : 'S';

  return (
    <div className="p-4 border-t border-[#E5E7EB] shrink-0 mt-auto bg-[#F9FAFB]">
      <div className="flex items-center gap-3 mb-4 px-2">
        <div className="w-10 h-10 rounded-full bg-spus-gold flex items-center justify-center text-white font-bold text-lg shadow-sm">
          {initial}
        </div>
        <div className="overflow-hidden">
          <p className="text-sm font-semibold text-gray-900 truncate">
            {user.name}
          </p>
          <p className="text-xs text-gray-500 font-medium truncate">
            {user.id}
          </p>
        </div>
      </div>
      
      <button
        onClick={onLogout}
        className="w-full py-2 border border-[#E5E7EB] rounded-lg bg-white text-gray-600 text-sm font-medium
                   flex items-center justify-center gap-2 transition hover:border-gray-300 hover:bg-gray-50"
      >
        <LogOut className="w-4 h-4" />
        Log Out
      </button>
    </div>
  );
}
