# OpenEvolve Frontend Setup Guide

This guide provides complete setup instructions for the OpenEvolve React frontend application.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your backend URL
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

## Detailed Setup Instructions

### Prerequisites

- Node.js 16 or higher
- npm 8 or higher
- OpenEvolve backend server running

### Step 1: Environment Configuration

Create a `.env` file in the frontend directory:

```bash
# Required: Backend API URL
REACT_APP_API_URL=http://localhost:8080

# Optional: Debug mode
REACT_APP_DEBUG=false
```

### Step 2: Install Dependencies

```bash
cd frontend
npm install
```

This installs all required dependencies including:
- React 18 with TypeScript
- Redux Toolkit for state management
- Styled Components for styling
- React Router for navigation
- Axios for API calls
- Testing libraries

### Step 3: Start Development Server

```bash
npm start
```

The application will start at `http://localhost:3000` and automatically open in your browser.

### Step 4: Verify Backend Connection

1. Open the application in your browser
2. Try to log in or register a new account
3. If you see connection errors, verify:
   - Backend server is running on the configured URL
   - CORS is properly configured on the backend
   - Environment variables are set correctly

## Backend Integration

### Required Backend Endpoints

The frontend expects these API endpoints to be available:

#### Authentication
- `POST /api/auth/login`
- `POST /api/auth/register`
- `GET /api/auth/verify`
- `POST /api/auth/logout`

#### Evolution Management
- `GET /api/evolution/runs`
- `POST /api/evolution/runs`
- `GET /api/evolution/runs/:id`
- `POST /api/evolution/runs/:id/stop`

#### Program Management
- `GET /api/programs`
- `GET /api/programs/:id`
- `GET /api/programs/:id/details`

### CORS Configuration

Ensure your backend allows requests from `http://localhost:3000` during development.

Example Express.js CORS configuration:
```javascript
app.use(cors({
  origin: ['http://localhost:3000', 'https://your-production-domain.com'],
  credentials: true
}));
```

## Development Workflow

### Running Tests

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm test -- --watch
```

### Code Quality

The project includes ESLint and Prettier for code quality:

```bash
# Lint code
npm run lint

# Format code
npm run format
```

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Project Structure

```
frontend/
├── public/                 # Static assets
│   ├── index.html         # HTML template
│   └── manifest.json      # PWA manifest
├── src/
│   ├── components/        # Reusable components
│   │   ├── Common/       # Generic UI components
│   │   ├── Layout/       # Layout components
│   │   └── Auth/         # Authentication components
│   ├── pages/            # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Evolution.tsx
│   │   ├── Programs.tsx
│   │   ├── Settings.tsx
│   │   └── Login.tsx
│   ├── store/            # Redux store
│   │   ├── store.ts      # Store configuration
│   │   └── slices/       # Redux slices
│   ├── services/         # API services
│   │   └── api.ts        # HTTP client and API methods
│   ├── hooks/            # Custom React hooks
│   ├── styles/           # Theme and styling
│   └── __tests__/        # Test files
├── package.json
├── tsconfig.json
└── README.md
```

## Key Features

### Authentication
- JWT-based authentication
- Protected routes
- Automatic token refresh
- Login/register forms

### Evolution Management
- Start and stop evolution runs
- Monitor progress in real-time
- View run statistics and metrics
- Configure evolution parameters

### Program Browsing
- View evolved programs
- Filter and sort by metrics
- Inspect program code and details
- Track program genealogy

### User Interface
- Responsive design for all devices
- Dark/light theme toggle
- Toast notifications
- Loading states and error handling

## Customization

### Theming

The application uses a comprehensive theme system. To customize:

1. Edit `src/styles/theme.ts`
2. Modify color palette, spacing, or typography
3. Changes apply automatically across all components

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation link in `src/components/Layout/Sidebar.tsx`

### API Integration

To add new API endpoints:

1. Add methods to `src/services/api.ts`
2. Create Redux slice if needed in `src/store/slices/`
3. Use in components with Redux hooks

## Troubleshooting

### Common Issues

1. **"Cannot connect to backend"**
   - Verify backend server is running
   - Check REACT_APP_API_URL in .env
   - Ensure CORS is configured correctly

2. **"Module not found" errors**
   - Delete node_modules and package-lock.json
   - Run `npm install` again
   - Check for TypeScript errors

3. **Build failures**
   - Run `npm run build` to see detailed errors
   - Fix TypeScript errors
   - Ensure all imports are correct

4. **Tests failing**
   - Run `npm test` to see specific failures
   - Check for missing test setup
   - Verify mock configurations

### Debug Mode

Enable debug mode for additional logging:

```bash
# In .env file
REACT_APP_DEBUG=true
```

This enables:
- Detailed API request/response logging
- Redux state change logging
- Performance monitoring

### Performance Issues

If the application feels slow:

1. Check browser dev tools for performance bottlenecks
2. Use React DevTools Profiler
3. Verify large lists are virtualized
4. Check for unnecessary re-renders

## Deployment

### Static Hosting (Recommended)

1. Build the application:
   ```bash
   npm run build
   ```

2. Deploy the `build/` directory to:
   - Netlify
   - Vercel
   - GitHub Pages
   - AWS S3 + CloudFront

### Docker Deployment

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Variables for Production

Set these environment variables in your deployment platform:

```bash
REACT_APP_API_URL=https://your-api-domain.com
REACT_APP_DEBUG=false
```

## Support

For issues or questions:

1. Check this documentation first
2. Review the troubleshooting section
3. Check the GitHub issues
4. Create a new issue with detailed information

## Next Steps

After setup:

1. Explore the example evolution runs
2. Try creating your own evolution configuration
3. Experiment with different visualization options
4. Customize the theme to match your preferences

The frontend is designed to be intuitive and self-explanatory, but don't hesitate to explore the codebase to understand how everything works together.