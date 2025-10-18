# URL-Based Images Guide

This guide explains how to use URL-based images for products and categories instead of uploading files directly.

## Benefits of URL-Based Images

✅ **Faster Loading**: Images served from CDNs load faster  
✅ **No Storage Costs**: No need to store images on your server  
✅ **Easy Management**: Update images by changing URLs  
✅ **Scalability**: No server storage limitations  
✅ **CDN Benefits**: Automatic optimization and global distribution  

## How It Works

Your system supports both file uploads and URL-based images:

1. **Product Images**: Use the `image_url` field instead of uploading files
2. **Category Images**: Use the `image_url` field (after migration)
3. **Automatic Fallback**: System prioritizes uploaded files over URLs if both exist

## Setting Up URL-Based Images

### 1. Apply Category Migration (if needed)

```bash
python backend/add_category_image_url_migration.py
```

### 2. Add Products with URLs

#### Option A: Use the Interactive Script
```bash
python add_url_based_products.py
```

#### Option B: Add Sample Products
The script can load from `backend/sample_products_with_urls.json`

#### Option C: Manual Django Admin
1. Go to Django Admin
2. Add/Edit Product
3. Leave `image` field empty
4. Fill in `image_url` field with your URL

### 3. Recommended Image Sources

#### Free Stock Photos
- **Unsplash**: `https://images.unsplash.com/photo-ID?w=400&h=400&fit=crop`
- **Pexels**: `https://images.pexels.com/photos/ID/photo.jpg?w=400&h=400&fit=crop`
- **Pixabay**: `https://pixabay.com/get/ID.jpg`

#### CDN Services
- **Cloudinary**: `https://res.cloudinary.com/your-cloud/image/upload/w_400,h_400,c_fill/your-image`
- **ImageKit**: `https://ik.imagekit.io/your-id/your-image?tr=w-400,h-400`
- **AWS S3 + CloudFront**: `https://your-cloudfront-domain.com/images/product.jpg`

#### Image Optimization Parameters
Most services support URL parameters for optimization:
- `w=400&h=400` - Set width and height
- `fit=crop` or `c_fill` - Crop to fit dimensions
- `q=80` - Set quality (80% recommended)
- `f=webp` - Convert to WebP format

## Example Product Data Structure

```json
{
  "id": "ent-tshirt-001",
  "title": "ENT Classic Black T-Shirt",
  "price": "25.99",
  "description": "Premium cotton t-shirt with ENT logo.",
  "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center",
  "category": "t-shirts",
  "stock_quantity": 50,
  "is_featured": true
}
```

## API Response

The API automatically handles URL-based images:

```json
{
  "id": "ent-tshirt-001",
  "title": "ENT Classic Black T-Shirt",
  "price": "25.99",
  "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center",
  "category": "t-shirts"
}
```

## Best Practices

### Image Specifications
- **Size**: 400x400px minimum (square format recommended)
- **Format**: JPEG, PNG, or WebP
- **Quality**: 80-90% for good balance of quality and file size
- **File Size**: Under 200KB for fast loading

### URL Guidelines
- Use HTTPS URLs for security
- Ensure URLs are permanent (don't change)
- Use CDN services for better performance
- Include optimization parameters in URLs
- Test URLs before adding to products

### Fallback Strategy
```python
# The system automatically handles fallbacks:
def get_image_url(self):
    if self.image:           # 1st priority: uploaded file
        return self.image.url
    elif self.image_url:     # 2nd priority: URL field
        return self.image_url
    else:                    # 3rd priority: placeholder
        return "https://via.placeholder.com/400x400/e5e7eb/6b7280?text=No+Image"
```

## Managing Images

### Adding New Products
1. Use the interactive script: `python add_url_based_products.py`
2. Or use Django Admin and fill the `image_url` field

### Updating Existing Products
1. Edit product in Django Admin
2. Clear the `image` field if you want to use URL
3. Add your URL to the `image_url` field

### Bulk Import
Create a JSON file similar to `backend/sample_products_with_urls.json` and use the script to import.

## Troubleshooting

### Image Not Showing
1. **Check URL**: Ensure the URL is accessible in browser
2. **HTTPS**: Make sure URL uses HTTPS
3. **CORS**: Some image hosts block cross-origin requests
4. **Permissions**: Ensure the image is publicly accessible

### Performance Issues
1. **Optimize URLs**: Add width/height parameters
2. **Use CDN**: Consider using a CDN service
3. **Image Format**: Use WebP format when possible
4. **Compression**: Ensure images are properly compressed

### Common URL Formats

#### Unsplash
```
https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center
```

#### Cloudinary
```
https://res.cloudinary.com/demo/image/upload/w_400,h_400,c_fill/sample.jpg
```

#### Custom CDN
```
https://your-cdn.com/images/product-001.jpg?w=400&h=400
```

## Migration from File Uploads

If you have existing products with uploaded files and want to switch to URLs:

1. **Backup**: Export your current product data
2. **Upload to CDN**: Upload existing images to your preferred CDN
3. **Update Products**: Replace file references with CDN URLs
4. **Test**: Verify all images load correctly
5. **Cleanup**: Remove old uploaded files if desired

## Security Considerations

- Use HTTPS URLs only
- Validate URLs before saving
- Consider hotlinking policies of image hosts
- Monitor for broken image links
- Have fallback images ready

## Performance Monitoring

Monitor your image loading performance:
- Use browser dev tools to check load times
- Consider lazy loading for better performance
- Monitor CDN usage and costs
- Set up alerts for broken image links

---

**Need Help?** 
- Run `python add_url_based_products.py` for interactive setup
- Check the Django Admin for manual management
- Review the API endpoints for programmatic access