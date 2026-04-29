const Skeleton = ({ className }) => {
  return (
    <div className={`animate-pulse bg-gray-200 rounded-2xl ${className}`}></div>
  );
};

export const ProductCardSkeleton = () => {
  return (
    <div className="bg-white rounded-3xl overflow-hidden shadow-lg border border-gray-100">
      <Skeleton className="w-full h-64" />
      <div className="p-6 space-y-4">
        <Skeleton className="w-24 h-4" />
        <Skeleton className="w-full h-8" />
        <div className="flex justify-between items-center">
          <Skeleton className="w-20 h-6" />
          <Skeleton className="w-24 h-10 rounded-xl" />
        </div>
      </div>
    </div>
  );
};

export default Skeleton;
