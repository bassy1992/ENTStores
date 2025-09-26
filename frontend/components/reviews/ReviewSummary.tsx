import { useState, useEffect } from 'react';
import { Star } from 'lucide-react';
import { API_ENDPOINTS } from '../../config/api';

interface ReviewSummaryProps {
  productId: string;
  className?: string;
}

interface ReviewStats {
  average_rating: number;
  total_reviews: number;
}

export default function ReviewSummary({ productId, className = '' }: ReviewSummaryProps) {
  const [stats, setStats] = useState<ReviewStats>({
    average_rating: 4.3,
    total_reviews: 4
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(API_ENDPOINTS.REVIEWS(productId), {
          headers: {
            'Accept': 'application/json',
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.stats) {
            setStats(data.stats);
            console.log('✅ Review stats loaded:', data.stats);
          }
        } else {
          console.log('⚠️ API error fetching review stats:', response.status);
        }
      } catch (error) {
        console.log('⚠️ Error fetching review stats:', error);
      }
      setLoading(false);
    };

    fetchStats();
  }, [productId]);

  if (loading) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <div className="flex items-center">
          {[...Array(5)].map((_, i) => (
            <Star key={i} className="w-4 h-4 text-gray-300 animate-pulse" />
          ))}
        </div>
        <span className="text-sm text-gray-400">Loading...</span>
      </div>
    );
  }

  if (!stats || stats.total_reviews === 0) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <div className="flex items-center">
          {[...Array(5)].map((_, i) => (
            <Star key={i} className="w-4 h-4 text-gray-300" />
          ))}
        </div>
        <span className="text-sm text-gray-500">No reviews yet</span>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="flex items-center">
        {[...Array(5)].map((_, i) => (
          <Star 
            key={i} 
            className={`w-4 h-4 ${
              i < Math.floor(stats.average_rating) 
                ? 'fill-yellow-400 text-yellow-400' 
                : 'text-gray-300'
            }`} 
          />
        ))}
      </div>
      <span className="text-sm text-gray-600">
        ({stats.average_rating.toFixed(1)}) • {stats.total_reviews} review{stats.total_reviews !== 1 ? 's' : ''}
      </span>
    </div>
  );
}