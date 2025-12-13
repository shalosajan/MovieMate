import React from "react";

export default function Modal({ open, onClose, children }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
      <div className="relative bg-gray-900 text-white rounded-lg p-6 max-w-3xl w-full">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-xl text-gray-300 hover:text-white"
        >
          ×
        </button>

        {children}
      </div>
    </div>
  );
}
