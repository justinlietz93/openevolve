# OpenEvolve Frontend

A modern React-based frontend application for the OpenEvolve evolutionary coding agent system.

## Features

- **Modern React Architecture**: Built with React 18, TypeScript, and Redux Toolkit
- **Responsive Design**: Mobile-first design that works on all devices
- **Dark/Light Theme**: Toggle between light and dark modes
- **Real-time Updates**: Live monitoring of evolution runs and program metrics
- **Interactive Visualizations**: View evolution progress and program relationships
- **Secure Authentication**: JWT-based authentication with protected routes
- **Performance Optimized**: Lazy loading, code splitting, and optimized bundle size

## Tech Stack

- **Frontend Framework**: React 18 with TypeScript
- **State Management**: Redux Toolkit
- **Styling**: Styled Components with CSS-in-JS
- **Routing**: React Router v6
- **HTTP Client**: Axios with interceptors
- **Testing**: Jest + React Testing Library
- **Build Tool**: Create React App (can be migrated to Vite)

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- OpenEvolve backend server running on `http://localhost:8080`

### Installation

1. **Clone and install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure:
   ```
   REACT_APP_API_URL=http://localhost:8080
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The application will open at `http://localhost:3000`

### Available Scripts

- `npm start` - Start development server
- `npm test` - Run test suite
- `npm run test:coverage` - Run tests with coverage report
- `npm run build` - Build for production
- `npm run eject` - Eject from Create React App (not recommended)

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Common/       # Generic components (Button, Input, etc.)
│   │   ├── Layout/       # Layout components (Header, Sidebar)
│   │   └── Auth/         # Authentication components
│   ├── pages/            # Page components
│   ├── store/            # Redux store and slices
│   ├── services/         # API services and HTTP client
│   ├── hooks/            # Custom React hooks
│   ├── styles/           # Theme and global styles
│   └── __tests__/        # Test files
├── package.json
└── README.md
```

## API Integration

The frontend integrates with the OpenEvolve backend through a comprehensive API client:

### Authentication API
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/verify` - Token verification
- `POST /api/auth/logout` - User logout

### Evolution API
- `GET /api/evolution/runs` - Get all evolution runs
- `POST /api/evolution/runs` - Start new evolution run
- `GET /api/evolution/runs/:id` - Get specific run details
- `POST /api/evolution/runs/:id/stop` - Stop evolution run

### Programs API
- `GET /api/programs` - Get programs for a run
- `GET /api/programs/:id` - Get program details
- `GET /api/programs/:id/code` - Get program source code

### Error Handling

The API client includes comprehensive error handling:
- Automatic token refresh
- Request/response interceptors
- Network error handling
- 401 redirect to login

## State Management

The application uses Redux Toolkit for state management with the following slices:

- **authSlice**: User authentication state
- **evolutionSlice**: Evolution runs and status
- **programsSlice**: Program data and filtering
- **uiSlice**: UI state (theme, toasts, loading)

## Component Architecture

### Common Components

- **Button**: Flexible button with variants and loading states
- **Input**: Form input with validation and error display
- **Card**: Container component with hover effects
- **LoadingSpinner**: Reusable loading indicator
- **Toast**: Notification system
- **ErrorBoundary**: Error handling wrapper

### Layout Components

- **Header**: Top navigation with user info and theme toggle
- **Sidebar**: Navigation sidebar with responsive behavior

### Page Components

- **Dashboard**: Overview of evolution runs an statistics
- **Evolution**: Manage and monitor evolution runs
- **Programs**: Browse and analyze evolved programs
- **Settings**: User preferences and configuration
- **Login**: Authentication interface

## Styling and Theming

The application uses Styled Components with a comprehensive theme system:

### Theme Structure
```typescript
{
  colors: {
    primary: '#3b5ca8',
    secondary: '#2196f3',
    success: '#4caf50',
    warning: '#ff9800',
    error: '#f44336',
    background: '#f5f5f5',
    surface: '#ffffff',
    text: {
      primary: '#333333',
      secondary: '#666666',
    },
    border: '#e0e0e0',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  // ... more theme properties
}
```

### Responsive Design

The application is fully responsive with breakpoints:
- Mobile: `768px`
- Tablet: `1024px`
- Desktop: `1200px`

## Testing

The application includes comprehensive testing:

### Test Coverage Goals
- **Components**: 80%+ coverage
- **Hooks**: 90%+ coverage
- **Store/Reducers**: 95%+ coverage
- **Utils**: 90%+ coverage

### Running Tests
```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm test -- --watch
```

### Test Structure
- Unit tests for components using React Testing Library
- Integration tests for user flows
- Hook testing with custom test utilities
- Redux store testing

## Performance Optimization

### Bundle Optimization
- Code splitting by route
- Lazy loading of heavy components
- Tree shaking for unused code
- Asset optimization

### Runtime Performance
- Memoization of expensive calculations
- Virtualization for large lists
- Debounced search inputs
- Optimized re-renders with React.memo

### Loading States
- Skeleton screens for better perceived performance
- Progressive loading of data
- Optimistic updates where appropriate

## Deployment

### Production Build
```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

### Environment Configuration

Create environment-specific `.env` files:

- `.env.development` - Development settings
- `.env.production` - Production settings
- `.env.local` - Local overrides (gitignored)

### Deployment Options

1. **Static Hosting** (Netlify, Vercel, GitHub Pages)
2. **CDN Deployment** (AWS CloudFront, Azure CDN)
3. **Container Deployment** (Docker, Kubernetes)

### Docker Deployment
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Security Considerations

### Authentication
- JWT tokens stored securely
- Automatic token refresh
- Protected routes with authentication guards

### API Security
- HTTPS enforcement in production
- CORS configuration
- Request/response sanitization

### Content Security
- XSS protection
- Content Security Policy headers
- Secure cookie settings

## Browser Compatibility

The application supports:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow the existing code style and patterns
2. Write tests for new features
3. Update documentation as needed
4. Use semantic commit messages
5. Ensure all tests pass before submitting PR

## Troubleshooting

### Common Issues

1. **API Connection Issues**
   - Verify backend server is running
   - Check CORS configuration
   - Validate environment variables

2. **Build Failures**
   - Clear node_modules and reinstall
   - Check for TypeScript errors
   - Verify all dependencies are compatible

3. **Performance Issues**
   - Use React DevTools Profiler
   - Check for unnecessary re-renders
   - Optimize large lists with virtualization

### Debug Mode

Enable debug mode by setting:
```bash
REACT_APP_DEBUG=true
```

This enables additional logging and development tools.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.