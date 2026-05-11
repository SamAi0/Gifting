import { Star } from 'lucide-react';

const StarRating = ({ rating, maxRating = 5, size = 16, className = "" }) => {
  return (
    <div className={`flex items-center gap-1 ${className}`}>
      {[...Array(maxRating)].map((_, i) => (
        <Star
          key={i}
          size={size}
          className={i < Math.floor(rating) ? "text-accent fill-accent" : "text-slate-200"}
        />
      ))}
      {rating > 0 && (
        <span className="ml-1 text-xs font-bold text-slate-500">{rating.toFixed(1)}</span>
      )}
    </div>
  );
};

export default StarRating;
