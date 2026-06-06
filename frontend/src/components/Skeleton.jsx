const Skeleton = ({ className }) => {
  return (
    <div className={`animate-pulse bg-slate-200 rounded-2xl ${className}`}></div>
  );
};

export const ProductCardSkeleton = () => {
  return (
    <div className="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-100 flex flex-col h-full">
      <Skeleton className="w-full aspect-square rounded-b-none" />
      <div className="p-5 flex flex-col flex-grow space-y-4">
        <Skeleton className="w-1/3 h-3" />
        <Skeleton className="w-full h-5" />
        <Skeleton className="w-2/3 h-4" />
        <div className="mt-auto pt-4 border-t border-slate-50 flex justify-between items-center">
          <Skeleton className="w-16 h-6" />
          <Skeleton className="w-10 h-10 rounded-xl" />
        </div>
      </div>
    </div>
  );
};

export default Skeleton;
