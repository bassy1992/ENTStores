import { useState, useEffect } from 'react';
import { Star, User, Calendar, CheckCircle, X } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { motion, AnimatePresence } from 'framer-motion';
import { API_BASE_URL, API_ENDPOINTS } from '../../config/api';

interface SimpleReviewSystemProps {
  productId: string;
  productSlug: string;
}

export default function SimpleReviewSystem({ productId, productSlug }: SimpleReviewSystemProps) {
  const [loading, setLoading] = useState(true);
  const [showWriteReview, setShowWriteReview] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'highest' | 'lowest' | 'helpful'>('newest');
  const [filterRating, setFilterRating] = useState<number | null>(null);
  const [reviews, setReviews] = useState([]);
  const [reviewStats, setReviewStats] = useState({
    average_rating: 0,
    total_reviews: 0,
    rating_distribution: { 5: 0, 4: 0, 3: 0, 2: 0, 1: 0 }
  });

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

  useEffect(() => {
    const fetchReviews = async () => {
      setLoading(true);
      
      const url = `${API_ENDPOINTS.REVIEWS(productId)}?sort=${sortBy}${filterRating ? `&rating=${filterRating}` : ''}`;
      
      console.log('🔍 LOADING REVIEWS:');
      console.log('   API Base URL:', API_BASE_URL);
      console.log('   Full URL:', url);
      console.log('   Product ID:', productId);
      
      try {
        const response = await fetch(url, {
          headers: {
            'Accept': 'application/json',
          }
        });
        
        console.log('📡 Response Status:', response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log('📊 API Response:', data);
          
          if (data.reviews) {
            setReviews(data.reviews);
            console.log(`✅ SUCCESS! Loaded ${data.reviews.length} reviews from backend`);
          } else {
            setReviews([]);
            console.log('⚠️ API returned no reviews data');
          }
          
          if (data.stats) {
            setReviewStats(data.stats);
            console.log('📊 Review stats loaded:', data.stats);
          }
        } else {
          const errorText = await response.text();
          console.error('❌ API Error:', response.status, errorText);
          setReviews([]);
        }
      } catch (error) {
        console.error('❌ Network Error:', error);
        setReviews([]);
      }
      
      setLoading(false);
    };

    fetchReviews();
  }, [productId, sortBy, filterRating]);

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newReview.rating === 0) return;

    setSubmitting(true);
    
    const reviewData = {
      user_name: newReview.user_name,
      user_email: newReview.user_email,
      rating: newReview.rating,
      title: newReview.title,
      comment: newReview.comment,
      size_purchased: newReview.size_purchased,
      color_purchased: newReview.color_purchased
    };
    
    const url = API_ENDPOINTS.REVIEWS(productId);
    
    console.log('🚀 SUBMITTING REVIEW:');
    console.log('   API Base URL:', API_BASE_URL);
    console.log('   Full URL:', url);
    console.log('   Product ID:', productId);
    console.log('   Review Data:', reviewData);
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(reviewData)
      });

      console.log('📡 Response Status:', response.status);
      console.log('📡 Response Headers:', Object.fromEntries(response.headers.entries()));

      if (response.ok) {
        const result = await response.json();
        console.log('✅ SUCCESS! Review submitted to backend:', result);
        setSubmitSuccess(true);
        
        // Refresh reviews after successful submission
        setTimeout(() => {
          console.log('🔄 Reloading page to show new review...');
          window.location.reload();
        }, 2000);
      } else {
        const errorText = await response.text();
        console.error('❌ BACKEND ERROR:', response.status, errorText);
        
        // Show error to user instead of fallback
        alert(`Failed to submit review: ${response.status} - ${errorText}`);
        setSubmitting(false);
        return;
      }
    } catch (error) {
      console.error('❌ NETWORK ERROR:', error);
      
      // Show error to user instead of silent fallback
      alert(`Network error: ${error.message}`);
      setSubmitting(false);
      return;
    }
    
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

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

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

  // Use dynamic stats instead of calculating from reviews
  const avgRating = reviewStats.average_rating;

  return (
    <div className="space-y-6">
      {/* Review Summary */}
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
                <div className="text-4xl font-bold">{avgRating.toFixed(1)}</div>
                <div>
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-5 h-5 ${
                          i < Math.floor(avgRating) 
                            ? 'fill-yellow-400 text-yellow-400' 
                            : 'text-gray-300'
                        }`} 
                      />
                    ))}
                  </div>
                  <p className="text-sm text-gray-600">
                    Based on {reviewStats.total_reviews} review{reviewStats.total_reviews !== 1 ? 's' : ''}
                  </p>
                </div>
              </div>
            </div>

            {/* Rating Distribution */}
            <div className="space-y-2">
              {[5, 4, 3, 2, 1].map(rating => {
                const count = reviewStats.rating_distribution[rating] || 0;
                const percentage = reviewStats.total_reviews > 0 ? (count / reviewStats.total_reviews) * 100 : 0;
                
                return (
                  <div key={rating} className="flex items-center gap-2 text-sm">
                    <span className="w-8">{rating}</span>
                    <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-yellow-400 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                    <span className="w-8 text-right">{count}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </CardContent>
      </Card>

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
                  <X className="w-5 h-5" />
                </Button>
              </div>

              {submitSuccess ? (
                <div className="text-center py-8">
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <h4 className="text-lg font-semibold text-green-700 mb-2">
                    Thank you for your review!
                  </h4>
                  <p className="text-gray-600">
                    Your review has been submitted successfully.
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

      {/* Reviews List */}
      <div className="space-y-4">
        {reviews.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <div className="text-gray-500">
                <h3 className="text-lg font-medium mb-2">No reviews yet</h3>
                <p className="text-sm">Be the first to review this product!</p>
                <button
                  onClick={() => setShowWriteReview(true)}
                  className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium"
                >
                  Write the First Review
                </button>
              </div>
            </CardContent>
          </Card>
        ) : (
          reviews.map((review) => (
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
                    {formatDate(review.created_at)}
                  </div>
                </div>

                {/* Review Content */}
                <p className="text-gray-700 leading-relaxed">{review.comment}</p>
              </div>
            </CardContent>
          </Card>
          ))
        )}
      </div>
    </div>
  );
}