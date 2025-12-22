# LOOM Mobile Optimization Guide

## Overview

LOOM is fully optimized for mobile devices, allowing you to manage your life from your phone browser without needing to start your computer. The application uses responsive design to provide an excellent experience on all screen sizes.

## Mobile Features

### Responsive Design
- **Touch-Optimized**: All buttons and interactive elements meet the 44x44px minimum touch target size
- **Adaptive Layouts**: Content automatically adjusts for phones, tablets, and desktops
- **Mobile Navigation**: Compact, scrollable navigation that works on small screens
- **Single-Column Layouts**: Cards stack vertically on mobile for easy scrolling

### Device Support
- ✅ **iOS Safari** (iPhone, iPad)
- ✅ **Android Chrome** (All Android devices)
- ✅ **Mobile Firefox**
- ✅ **Samsung Internet**
- ✅ **Other mobile browsers**

### Screen Sizes Supported
- **Small phones** (320px - 480px): iPhone SE, small Android phones
- **Standard phones** (481px - 768px): iPhone 12/13/14, most Android phones
- **Tablets** (769px - 1024px): iPad, Android tablets
- **Desktop** (1025px+): Full desktop experience

## Mobile-Specific Optimizations

### Navigation
- **Compact Mode**: Logo and menu items automatically resize on mobile
- **Wrapped Menu**: Navigation items wrap to multiple lines if needed
- **Touch Feedback**: Visual feedback when tapping navigation items
- **No Hover Effects**: Hover effects disabled on touch devices to prevent sticky states

### Dashboard
- **Stacked Cards**: All dashboard cards stack vertically on mobile
- **Easy Scanning**: Larger text and spacing for comfortable reading
- **Quick Access**: Touch any item to view details
- **Empty States**: Clear messages when no data is available

### Forms & Inputs
- **No Zoom on Focus**: Input fields use 16px font size to prevent iOS auto-zoom
- **Full-Width Fields**: All form fields expand to full width on mobile
- **Clear Focus States**: Blue highlight when editing fields
- **Touch-Friendly Buttons**: Large, easy-to-tap buttons

### Content
- **Single Column**: Notes, todos, and other content display in a single column
- **Touch Targets**: Minimum 60px height for all tappable items
- **Readable Text**: Optimized font sizes for mobile screens
- **Smooth Scrolling**: Native smooth scrolling for better performance

## Accessing LOOM on Mobile

### From Your Phone

1. **Connect to Your Home Network**
   - Make sure your phone is on the same WiFi network as your NAS

2. **Open Your Browser**
   - Works best with Safari (iOS) or Chrome (Android)

3. **Navigate to LOOM**
   ```
   http://<your-nas-ip>:5847
   ```
   Example: `http://192.168.1.100:5847`

4. **Add to Home Screen** (Optional but recommended)

   **On iOS (Safari):**
   - Tap the Share button (square with arrow)
   - Scroll down and tap "Add to Home Screen"
   - Name it "LOOM" and tap "Add"
   - LOOM will now appear as an app icon on your home screen

   **On Android (Chrome):**
   - Tap the menu button (three dots)
   - Tap "Add to Home screen"
   - Name it "LOOM" and tap "Add"
   - LOOM will appear as an app icon in your app drawer

### Benefits of Adding to Home Screen
- **App-Like Experience**: Opens in full-screen mode without browser UI
- **Quick Access**: Launch LOOM like a native app
- **Stay Signed In**: Keeps your session active
- **Dark Status Bar**: Matches LOOM's dark theme

## Mobile Usage Tips

### Quick Actions
- **Tap**: Select items, navigate, or trigger actions
- **Swipe**: Scroll through lists and pages
- **Pull to Refresh**: Refresh data by pulling down (if implemented)

### Best Practices
1. **Use Portrait Mode**: Most screens are optimized for portrait orientation
2. **Landscape Works Too**: Landscape mode is fully supported with optimized layouts
3. **One-Handed Use**: Navigation is positioned for easy thumb access
4. **Quick Edits**: Make quick changes without needing your computer

### Performance
- **Fast Loading**: Optimized for mobile network speeds
- **Minimal Data**: Efficient API calls to reduce data usage
- **Smooth Animations**: Hardware-accelerated transitions
- **Battery Friendly**: Efficient rendering to preserve battery life

## Mobile Breakpoints

The application uses the following responsive breakpoints:

```css
Desktop (default):  1025px and up
Tablet:            769px - 1024px
Mobile:            up to 768px
Small Mobile:      up to 480px
Landscape Mobile:  up to 896px (landscape orientation)
```

## Touch Gestures

### Supported Gestures
- ✅ **Tap**: Standard selection and navigation
- ✅ **Scroll**: Vertical scrolling through content
- ✅ **Pull**: Pull to see more content

### Visual Feedback
- **Active States**: Buttons slightly scale down when tapped
- **Highlight Color**: Blue highlight on active elements
- **No Text Selection**: Prevents accidental text selection on tap targets

## Accessibility

### Mobile Accessibility Features
- **Large Touch Targets**: Minimum 44x44px for all interactive elements
- **High Contrast**: Dark mode with excellent color contrast
- **Readable Font Sizes**: Minimum 16px to prevent zoom
- **Clear Focus States**: Visible focus indicators for keyboard navigation
- **Semantic HTML**: Proper heading hierarchy and landmarks

## Troubleshooting

### Page Zooms on Input Focus (iOS)
**Fixed**: All input fields use 16px font size to prevent auto-zoom.

### Navigation Feels Cramped
**Solution**: Navigation automatically wraps to multiple lines on small screens.

### Content Too Small to Read
**Check**: Your browser zoom level. Reset to 100% for optimal display.

### App Doesn't Load
**Verify**:
1. You're on the same network as your NAS
2. The NAS IP address is correct
3. Port 5847 is not blocked by firewall
4. Docker container is running

### Slow Performance
**Tips**:
- Close other browser tabs
- Clear browser cache
- Check your WiFi connection strength
- Restart the LOOM Docker container

## Remote Access (Optional)

### VPN Access
To access LOOM when away from home:
1. Set up VPN on your NAS (Synology VPN Server, WireGuard, etc.)
2. Connect to your home network via VPN on your phone
3. Access LOOM at `http://<nas-ip>:5847` as usual

### Security Note
⚠️ **Do NOT expose LOOM directly to the internet without proper authentication and HTTPS**. Always use VPN for remote access.

## Future Mobile Enhancements

Planned improvements:
- [ ] Pull-to-refresh functionality
- [ ] Offline mode with service workers
- [ ] Push notifications for reminders
- [ ] Native app feel with PWA
- [ ] Gesture navigation (swipe to go back)
- [ ] Voice input for notes and todos

## Technical Details

### Meta Tags
The application includes mobile-optimized meta tags:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#1a1d29">
```

### CSS Features
- **Flexbox & Grid**: Modern layout techniques
- **Media Queries**: Responsive breakpoints
- **Touch Events**: Optimized for touch devices
- **Smooth Scrolling**: Native momentum scrolling
- **Hardware Acceleration**: GPU-accelerated animations

---

**Enjoy managing your life from anywhere with LOOM's mobile-optimized interface!**
