import { useState, useEffect } from 'react';
import { Star, User, Calendar } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';

interface SimpleReviewSystemProps {
  productId: string;
  productSlug: string;
}

export default function SimpleReviewSystem({ productId, productSlug }: SimpleReviewSystemProps) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <Card>
        <CardContent className="p-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading reviews...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Review Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Customer Reviews</span>
            <Button className="bg-blue-600 hover:bg-blue-700">
              Write a Review
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            {/* Overall Rating */}
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="text-4xl font-bold">4.3</div>
                <div>
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-5 h-5 ${
                          i < 4 
                            ? 'fill-yellow-400 text-yellow-400' 
                            : 'text-gray-300'
                        }`} 
                      />
                    ))}
                  </div>
                  <p className="text-sm text-gray-600">
                    Based on 4 reviews
                  </p>
                </div>
              </div>
            </div>

            {/* Rating Distribution */}
            <div className="space-y-2">
              {[5, 4, 3, 2, 1].map(rating => (
                <div key={rating} className="flex items-center gap-2 text-sm">
                  <span className="w-8">{rating}</span>
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-yellow-400 h-2 rounded-full transition-all duration-300"
                      style={{ 
                        width: `${rating === 5 ? 50 : rating === 4 ? 25 : rating === 3 ? 25 : 0}%` 
                      }}
                    />
                  </div>
                  <span className="w-8 text-right">
                    {rating === 5 ? 2 : rating === 4 ? 1 : rating === 3 ? 1 : 0}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Sample Reviews */}
      <div className="space-y-4">
        {[
          {
            id: '1',
            user_name: 'Sarah M.',
            rating: 5,
            title: 'Amazing quality!',
            comment: 'This product exceeded my expectations. The material is soft and comfortable, and the fit is perfect.',
            created_at: '2024-01-15T10:30:00Z',
            verified_purchase: true
          },
          {
            id: '2',
            user_name: 'Mike R.',
            rating: 4,
            title: 'Good value for money',
            comment: 'Nice product overall. The color is exactly as shown in the pictures.',
            created_at: '2024-01-10T14:20:00Z',
            verified_purchase: true
          }
        ].map((review) => (
          <Card key={review.id}>
            <CardContent className="p-6">
              <div className="space-y-4">
                {/* Review Header */}
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <Star 
                            key={i} 
                            className={`w-4 h-4 ${
                              i < review.rating 
                                ? 'fill-yellow-400 text-yellow-400' 
                                : 'text-gray-300'
                            }`} 
                          />
                        ))}
                      </div>
                      <span className="font-medium">{review.title}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <User className="w-4 h-4" />
                      <span>{review.user_name}</span>
                      {review.verified_purchase && (
                        <Badge variant="secondary" className="text-xs bg-green-100 text-green-700">
                          Verified Purchase
                        </Badge>
                      )}
                    </div>
                  </div>
                  <div className="text-sm text-gray-500 flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    Jan 15, 2024
                  </div>
                </div>

                {/* Review Content */}
                <p className="text-gray-700 leading-relaxed">{review.comment}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}