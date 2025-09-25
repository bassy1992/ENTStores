import { useState, useEffect } from 'react';
import { Star, ThumbsUp, ThumbsDown, User, Calendar, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Separator } from '../ui/separator';
import { Textarea } from '../ui/textarea';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { motion, AnimatePresence } from 'framer-motion';

interface Review {
  id: string;
  user_name: string;
  user_email?: string;
  rating: number;
  title: string;
  comment: string;
  created_at: string;
  verified_purchase: boolean;
  helpful_count: number;
  not_helpful_count: number;
  user_found_helpful?: boolean | null;
  images?: string[];
  size_purchased?: string;
  color_purchased?: string;
}

interface ReviewStats {
  average_rating: number;
  total_reviews: number;
  rating_distribution: {
    5: number;
    4: number;
    3: number;
    2: number;
    1: number;
  };
}

interface ReviewSystemProps {
  productId: string;
  productSlug: string;
}

export default function ReviewSystem({ productId, productSlug }: ReviewSystemProps) {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [reviewStats, setReviewStats] = useState<ReviewStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [showWriteReview, setShowWriteReview] = useState(false);
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'highest' | 'lowest' | 'helpful'>('newest');
  const [filterRating, setFilterRating] = useState<number | null>(null);

  console.log('ReviewSystem component rendered with productId:', productId);
  
  // Write review form state
  const [newReview, setNewReview] = useState({
    rating: 0,
    title: '',
    comment: '',
    user_name: '',
    user_email: '',
    size_purchased: '',
    color_purchased: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  useEffect(() => {
    const fetchReviews = async () => {
      setLoading(true);
      
      // Use mock data for now - will be replaced with API calls later
      const mockReviews: Review[] = [
        {
          id: '1',
          user_name: 'Sarah M.',
          rating: 5,
          title: 'Amazing quality!',
          comment: 'This product exceeded my expectations. The material is soft and comfortable, and the fit is perfect. I\'ve washed it several times and it still looks brand new. Highly recommend!',
          created_at: '2024-01-15T10:30:00Z',
          verified_purchase: true,
          helpful_count: 12,
          not_helpful_count: 1,
          size_purchased: 'M',
          color_purchased: 'Green'
        },
        {
          id: '2',
          user_name: 'Mike R.',
          rating: 4,
          title: 'Good value for money',
          comment: 'Nice product overall. The color is exactly as shown in the pictures. Only minor complaint is that it runs slightly small, so consider sizing up.',
          created_at: '2024-01-10T14:20:00Z',
          verified_purchase: true,
          helpful_count: 8,
          not_helpful_count: 0,
          size_purchased: 'L',
          color_purchased: 'Green'
        },
        {
          id: '3',
          user_name: 'Jennifer K.',
          rating: 5,
          title: 'Perfect fit and style',
          comment: 'Love this! The design is exactly what I was looking for. Fast shipping and great customer service too.',
          created_at: '2024-01-08T09:15:00Z',
          verified_purchase: true,
          helpful_count: 15,
          not_helpful_count: 0,
          size_purchased: 'S',
          color_purchased: 'Green'
        },
        {
          id: '4',
          user_name: 'David L.',
          rating: 3,
          title: 'Decent but not exceptional',
          comment: 'It\'s okay. The quality is decent for the price, but I\'ve seen better. The color faded a bit after a few washes.',
          created_at: '2024-01-05T16:45:00Z',
          verified_purchase: false,
          helpful_count: 3,
          not_helpful_count: 2,
          size_purchased: 'XL',
          color_purchased: 'Green'
        }
      ];

      const mockStats: ReviewStats = {
        average_rating: 4.25,
        total_reviews: 4,
        rating_distribution: {
          5: 2,
          4: 1,
          3: 1,
          2: 0,
          1: 0
        }
      };

      // Simulate loading time
      await new Promise(resolve => setTimeout(resolve, 500));

      setReviews(mockReviews);
      setReviewStats(mockStats);
      setLoading(false);
    };

    fetchReviews();
  }, [productId, sortBy, filterRating]);

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newReview.rating === 0) return;

    setSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Create new review
    const review: Review = {
      id: Date.now().toString(),
      user_name: newReview.user_name,
      rating: newReview.rating,
      title: newReview.title,
      comment: newReview.comment,
      created_at: new Date().toISOString(),
      verified_purchase: false,
      helpful_count: 0,
      not_helpful_count: 0,
      size_purchased: newReview.size_purchased,
      color_purchased: newReview.color_purchased
    };

    setReviews(prev => [review, ...prev]);
    setSubmitSuccess(true);
    setSubmitting(false);
    
    // Reset form
    setNewReview({
      rating: 0,
      title: '',
      comment: '',
      user_name: '',
      user_email: '',
      size_purchased: '',
      color_purchased: ''
    });

    setTimeout(() => {
      setShowWriteReview(false);
      setSubmitSuccess(false);
    }, 2000);
  };

  const handleHelpfulVote = async (reviewId: string, helpful: boolean) => {
    // Update review counts immediately
    setReviews(prev => prev.map(review => 
      review.id === reviewId 
        ? {
            ...review,
            helpful_count: helpful ? review.helpful_count + 1 : review.helpful_count,
            not_helpful_count: !helpful ? review.not_helpful_count + 1 : review.not_helpful_count,
            user_found_helpful: helpful
          }
        : review
    ));
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const sortedAndFilteredReviews = reviews
    .filter(review => filterRating ? review.rating === filterRating : true)
    .sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        case 'oldest':
          return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        case 'highest':
          return b.rating - a.rating;
        case 'lowest':
          return a.rating - b.rating;
        case 'helpful':
          return b.helpful_count - a.helpful_count;
        default:
          return 0;
      }
    });

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

  // Debug: Show component is rendering
  console.log('ReviewSystem rendering with reviews:', reviews.length, 'stats:', reviewStats);

  // Simple test to ensure component renders
  if (!productId) {
    return (
      <Card>
        <CardContent className="p-8">
          <p className="text-center text-gray-600">Product ID is required to load reviews.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Debug info */}
      <div className="text-xs text-gray-400 mb-4">
        Debug: ProductId: {productId}, Reviews: {reviews.length}, Loading: {loading.toString()}
      </div>
      
      {/* Review Summary */}
      {reviewStats && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Customer Reviews</span>
              <Button 
                onClick={() => setShowWriteReview(true)}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Write a Review
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 md:grid-cols-2">
              {/* Overall Rating */}
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  <div className="text-4xl font-bold">{reviewStats.average_rating.toFixed(1)}</div>
                  <div>
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star 
                          key={i} 
                          className={`w-5 h-5 ${
                            i < Math.floor(reviewStats.average_rating) 
                              ? 'fill-yellow-400 text-yellow-400' 
                              : 'text-gray-300'
                          }`} 
                        />
                      ))}
                    </div>
                    <p className="text-sm text-gray-600">
                      Based on {reviewStats.total_reviews} reviews
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
                          width: `${(reviewStats.rating_distribution[rating as keyof typeof reviewStats.rating_distribution] / reviewStats.total_reviews) * 100}%` 
                        }}
                      />
                    </div>
                    <span className="w-8 text-right">
                      {reviewStats.rating_distribution[rating as keyof typeof reviewStats.rating_distribution]}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Write Review Modal */}
      <AnimatePresence>
        {showWriteReview && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            onClick={() => setShowWriteReview(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold">Write a Review</h3>
                <Button 
                  variant="ghost" 
                  onClick={() => setShowWriteReview(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </Button>
              </div>

              {submitSuccess ? (
                <div className="text-center py-8">
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <h4 className="text-lg font-semibold text-green-700 mb-2">
                    Thank you for your review!
                  </h4>
                  <p className="text-gray-600">
                    Your review has been submitted and will be published after moderation.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleSubmitReview} className="space-y-4">
                  {/* Rating */}
                  <div>
                    <Label className="text-base font-medium">Overall Rating *</Label>
                    <div className="flex items-center gap-1 mt-2">
                      {[1, 2, 3, 4, 5].map(rating => (
                        <button
                          key={rating}
                          type="button"
                          onClick={() => setNewReview(prev => ({ ...prev, rating }))}
                          className="p-1 hover:scale-110 transition-transform"
                        >
                          <Star 
                            className={`w-8 h-8 ${
                              rating <= newReview.rating 
                                ? 'fill-yellow-400 text-yellow-400' 
                                : 'text-gray-300 hover:text-yellow-300'
                            }`} 
                          />
                        </button>
                      ))}
                      {newReview.rating > 0 && (
                        <span className="ml-2 text-sm text-gray-600">
                          {newReview.rating} star{newReview.rating !== 1 ? 's' : ''}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Review Title */}
                  <div>
                    <Label htmlFor="title">Review Title *</Label>
                    <Input
                      id="title"
                      value={newReview.title}
                      onChange={(e) => setNewReview(prev => ({ ...prev, title: e.target.value }))}
                      placeholder="Summarize your experience"
                      required
                    />
                  </div>

                  {/* Review Comment */}
                  <div>
                    <Label htmlFor="comment">Your Review *</Label>
                    <Textarea
                      id="comment"
                      value={newReview.comment}
                      onChange={(e) => setNewReview(prev => ({ ...prev, comment: e.target.value }))}
                      placeholder="Tell others about your experience with this product..."
                      rows={4}
                      required
                    />
                  </div>

                  {/* User Details */}
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label htmlFor="user_name">Your Name *</Label>
                      <Input
                        id="user_name"
                        value={newReview.user_name}
                        onChange={(e) => setNewReview(prev => ({ ...prev, user_name: e.target.value }))}
                        placeholder="Your name"
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="user_email">Email (optional)</Label>
                      <Input
                        id="user_email"
                        type="email"
                        value={newReview.user_email}
                        onChange={(e) => setNewReview(prev => ({ ...prev, user_email: e.target.value }))}
                        placeholder="your@email.com"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        We'll never share your email publicly
                      </p>
                    </div>
                  </div>

                  {/* Purchase Details */}
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label htmlFor="size_purchased">Size Purchased (optional)</Label>
                      <Input
                        id="size_purchased"
                        value={newReview.size_purchased}
                        onChange={(e) => setNewReview(prev => ({ ...prev, size_purchased: e.target.value }))}
                        placeholder="e.g., M, L, XL"
                      />
                    </div>
                    <div>
                      <Label htmlFor="color_purchased">Color Purchased (optional)</Label>
                      <Input
                        id="color_purchased"
                        value={newReview.color_purchased}
                        onChange={(e) => setNewReview(prev => ({ ...prev, color_purchased: e.target.value }))}
                        placeholder="e.g., Green, Blue"
                      />
                    </div>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <Button
                      type="submit"
                      disabled={submitting || newReview.rating === 0 || !newReview.title || !newReview.comment || !newReview.user_name}
                      className="flex-1"
                    >
                      {submitting ? (
                        <div className="flex items-center gap-2">
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                          Submitting...
                        </div>
                      ) : (
                        'Submit Review'
                      )}
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setShowWriteReview(false)}
                      disabled={submitting}
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Filters and Sorting */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-2">
              <Label className="text-sm font-medium">Sort by:</Label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="text-sm border rounded px-2 py-1"
              >
                <option value="newest">Newest</option>
                <option value="oldest">Oldest</option>
                <option value="highest">Highest Rating</option>
                <option value="lowest">Lowest Rating</option>
                <option value="helpful">Most Helpful</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <Label className="text-sm font-medium">Filter by rating:</Label>
              <div className="flex gap-1">
                <Button
                  variant={filterRating === null ? "default" : "outline"}
                  size="sm"
                  onClick={() => setFilterRating(null)}
                >
                  All
                </Button>
                {[5, 4, 3, 2, 1].map(rating => (
                  <Button
                    key={rating}
                    variant={filterRating === rating ? "default" : "outline"}
                    size="sm"
                    onClick={() => setFilterRating(rating)}
                    className="flex items-center gap-1"
                  >
                    {rating} <Star className="w-3 h-3" />
                  </Button>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Reviews List */}
      <div className="space-y-4">
        {sortedAndFilteredReviews.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No reviews found</h3>
              <p className="text-gray-600 mb-4">
                {filterRating 
                  ? `No reviews with ${filterRating} star${filterRating !== 1 ? 's' : ''} found.`
                  : 'Be the first to review this product!'
                }
              </p>
              <Button onClick={() => setShowWriteReview(true)}>
                Write the First Review
              </Button>
            </CardContent>
          </Card>
        ) : (
          sortedAndFilteredReviews.map((review, index) => (
            <motion.div
              key={review.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <Card>
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
                              <CheckCircle className="w-3 h-3 mr-1" />
                              Verified Purchase
                            </Badge>
                          )}
                        </div>
                      </div>
                      <div className="text-sm text-gray-500 flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {formatDate(review.created_at)}
                      </div>
                    </div>

                    {/* Purchase Details */}
                    {(review.size_purchased || review.color_purchased) && (
                      <div className="flex gap-2">
                        {review.size_purchased && (
                          <Badge variant="outline" className="text-xs">
                            Size: {review.size_purchased}
                          </Badge>
                        )}
                        {review.color_purchased && (
                          <Badge variant="outline" className="text-xs">
                            Color: {review.color_purchased}
                          </Badge>
                        )}
                      </div>
                    )}

                    {/* Review Content */}
                    <p className="text-gray-700 leading-relaxed">{review.comment}</p>

                    <Separator />

                    {/* Helpful Votes */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <span className="text-sm text-gray-600">Was this review helpful?</span>
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleHelpfulVote(review.id, true)}
                            disabled={review.user_found_helpful !== null}
                            className={`flex items-center gap-1 ${
                              review.user_found_helpful === true ? 'bg-green-50 border-green-200' : ''
                            }`}
                          >
                            <ThumbsUp className="w-3 h-3" />
                            Yes ({review.helpful_count})
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleHelpfulVote(review.id, false)}
                            disabled={review.user_found_helpful !== null}
                            className={`flex items-center gap-1 ${
                              review.user_found_helpful === false ? 'bg-red-50 border-red-200' : ''
                            }`}
                          >
                            <ThumbsDown className="w-3 h-3" />
                            No ({review.not_helpful_count})
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}