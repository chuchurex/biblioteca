---
name: performance-turbo
description: "Automatic performance optimization using AI analysis"
---

# Performance Turbo Command

Automatic performance optimization using advanced AI to achieve perfect performance without manual effort.

## Description

The `/performance-turbo` command takes your application's performance to the next level:

- **Automatic analysis** of bottlenecks and optimization opportunities
- **Intelligent optimizations** that preserve functionality
- **Automatic bundle optimization** for web apps
- **Database query optimization** for backend
- **Memory management** and leak prevention
- **Automatic lazy loading** of resources
- **AI-optimized caching strategies**
- **Integrated performance monitoring**
- **Web Vitals optimization** for SEO and UX
- **Real-time suggestions** during development

## Usage

```
/performance-turbo [directory] [--target] [--focus] [--budget] [--mode]
```

### Parameters

- `directory`: specific directory to optimize
- `--target`: Target platform (web, mobile, desktop, ssr)
- `--focus`: Area of focus (bundle, runtime, memory, network, database)
- `--budget`: Performance budget (strict, moderate, relaxed)
- `--mode`: Optimization mode (safe, aggressive, experimental)
- `--preserve`: Preserve specific functionality
- `--metrics`: Target metrics (lcp, fid, cls, ttfb)
- `--baseline`: Compare with previous baseline

### Examples

```
/performance-turbo
/performance-turbo src/ --target=web --focus=bundle --budget=strict
/performance-turbo backend/ --focus=database --mode=aggressive
/performance-turbo --target=mobile --metrics=lcp,fid --budget=strict
/performance-turbo components/ --focus=runtime --mode=safe
/performance-turbo api/ --focus=network --preserve=backward-compatibility
```

## Automatic Optimizations

### ⚡ Bundle Optimization
```javascript
// ❌ BEFORE - Unoptimized Bundle
import { entireLibrary } from 'heavy-library';
import './styles.css';
import './unused-styles.css';

const MyComponent = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    entireLibrary.fetchData().then(setData);
  }, []);
  
  return (
    <div className="container">
      {data.map(item => (
        <HeavyComponent key={item.id} item={item} />
      ))}
    </div>
  );
};

// ✅ AFTER - Automatically Optimized Bundle
import { fetchData } from 'heavy-library/fetch-only'; // Tree-shaking applied
import './styles.css'; // unused-styles.css automatically removed

const MyComponent = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    fetchData().then(setData);
  }, []);
  
  // Virtualization automatically added for large lists
  return (
    <VirtualizedList 
      items={data}
      renderItem={({ item }) => (
        <Suspense fallback={<ItemSkeleton />}>
          <HeavyComponent item={item} />
        </Suspense>
      )}
      className="container"
    />
  );
};

// Code splitting automatically added
const HeavyComponent = lazy(() => 
  import('./HeavyComponent').then(module => ({
    default: module.HeavyComponent
  }))
);
```

### 🧠 Memory Optimization
```javascript
// ❌ BEFORE - Memory inefficient
const DataProcessor = ({ items }) => {
  const [processedData, setProcessedData] = useState([]);
  const [cache, setCache] = useState({});
  
  const processItems = useCallback(() => {
    // Creates new objects on each render
    const processed = items.map(item => ({
      ...item,
      processed: heavyComputation(item),
      timestamp: Date.now()
    }));
    setProcessedData(processed);
  }, [items]);
  
  return (
    <div>
      {processedData.map(item => (
        <ItemComponent key={item.id} item={item} />
      ))}
    </div>
  );
};

// ✅ AFTER - Automatically Optimized Memory
const DataProcessor = ({ items }) => {
  // Intelligent memoization added
  const processedData = useMemo(() => {
    return items.map(item => ({
      ...item,
      processed: heavyComputation(item)
    }));
  }, [items]);
  
  // LRU cache automatically added
  const memoizedHeavyComputation = useMemo(() => 
    memoize(heavyComputation, { maxSize: 100 }), []
  );
  
  // Virtualization for large lists
  const virtualizedItems = useVirtualization(processedData, {
    itemHeight: 60,
    overscan: 5
  });
  
  return (
    <VirtualizedContainer>
      {virtualizedItems.map(({ item, index, style }) => (
        <div key={item.id} style={style}>
          <MemoizedItemComponent item={item} />
        </div>
      ))}
    </VirtualizedContainer>
  );
};

// Automatically memoized component
const MemoizedItemComponent = memo(ItemComponent, (prev, next) => 
  prev.item.id === next.item.id && 
  prev.item.version === next.item.version
);
```

### 🌐 Network Optimization
```javascript
// ❌ BEFORE - Network inefficient
const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [comments, setComments] = useState([]);
  
  useEffect(() => {
    // Multiple sequential requests
    fetchUser(userId).then(setUser);
    fetchUserPosts(userId).then(setPosts);
    fetchUserComments(userId).then(setComments);
  }, [userId]);
  
  return (
    <div>
      <UserInfo user={user} />
      <UserPosts posts={posts} />
      <UserComments comments={comments} />
    </div>
  );
};

// ✅ AFTER - Automatically Optimized Network
const UserProfile = ({ userId }) => {
  // GraphQL automatically added for single request
  const { data, loading, error } = useQuery(GET_USER_PROFILE, {
    variables: { userId },
    // Automatically optimized cache
    fetchPolicy: 'cache-first',
    // Related prefetch
    onCompleted: (data) => {
      // Prefetch user connections
      prefetchUserConnections(data.user.id);
    }
  });
  
  // Optimized loading states
  if (loading) return <UserProfileSkeleton />;
  if (error) return <ErrorBoundary error={error} />;
  
  const { user, posts, comments } = data;
  
  return (
    <div>
      <UserInfo user={user} />
      {/* Lazy loading automatically added */}
      <Suspense fallback={<PostsSkeleton />}>
        <LazyUserPosts posts={posts} />
      </Suspense>
      <Suspense fallback={<CommentsSkeleton />}>
        <LazyUserComments comments={comments} />
      </Suspense>
    </div>
  );
};

// Service Worker added for caching
const cacheStrategy = new CacheFirst({
  cacheName: 'user-profiles',
  plugins: [{
    // Intelligent cache invalidation
    cacheWillUpdate: async ({ response }) => 
      response.status === 200 && response.headers.get('content-type')?.includes('application/json')
  }]
});
```

### 🗄️ Database Optimization
```javascript
// ❌ BEFORE - Database inefficient
const getUsersWithPosts = async () => {
  const users = await User.findAll(); // N+1 query problem
  
  const usersWithPosts = await Promise.all(
    users.map(async user => {
      const posts = await Post.findAll({ where: { userId: user.id } });
      return { ...user.toJSON(), posts };
    })
  );
  
  return usersWithPosts;
};

// ✅ AFTER - Automatically Optimized Database
const getUsersWithPosts = async () => {
  // Eager loading automatically added
  const users = await User.findAll({
    include: [{
      model: Post,
      // Limit added to prevent over-fetching
      limit: 10,
      order: [['createdAt', 'DESC']],
      // Optimized field selection
      attributes: ['id', 'title', 'summary', 'createdAt']
    }],
    // Automatically suggested indexes
    attributes: ['id', 'name', 'email', 'avatarUrl'],
    // Automatically added pagination
    limit: 50,
    offset: 0
  });
  
  return users;
};

// Automatically suggested indexes
/*
CREATE INDEX CONCURRENTLY idx_posts_user_created 
ON posts (user_id, created_at DESC) 
WHERE deleted_at IS NULL;

CREATE INDEX CONCURRENTLY idx_users_active
ON users (id, name, email) 
WHERE active = true;
*/

// Automatically added cache layer
const getCachedUsersWithPosts = async () => {
  const cacheKey = 'users_with_posts_v1';
  
  let cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  const users = await getUsersWithPosts();
  await redis.setex(cacheKey, 300, JSON.stringify(users)); // 5 min cache
  
  return users;
};
```

### 🎨 Rendering Optimization
```javascript
// ❌ BEFORE - Rendering inefficient
const Dashboard = ({ filters, sortBy, searchTerm }) => {
  const [data, setData] = useState([]);
  
  // Re-render on every prop change
  const filteredData = data
    .filter(item => item.category === filters.category)
    .filter(item => item.name.includes(searchTerm))
    .sort((a, b) => a[sortBy] - b[sortBy]);
  
  return (
    <div>
      {filteredData.map(item => (
        <ItemCard 
          key={item.id} 
          item={item}
          onUpdate={() => updateItem(item.id)}
        />
      ))}
    </div>
  );
};

// ✅ AFTER - Automatically Optimized Rendering
const Dashboard = ({ filters, sortBy, searchTerm }) => {
  const [data, setData] = useState([]);
  
  // Memoization of expensive computations
  const filteredData = useMemo(() => {
    return data
      .filter(item => item.category === filters.category)
      .filter(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => {
        const aVal = a[sortBy];
        const bVal = b[sortBy];
        return typeof aVal === 'string' ? aVal.localeCompare(bVal) : aVal - bVal;
      });
  }, [data, filters.category, searchTerm, sortBy]);
  
  // Memoized callback
  const handleUpdate = useCallback((itemId) => {
    updateItem(itemId);
  }, []);
  
  // Virtualization for large lists
  const rowRenderer = useCallback(({ index, key, style }) => (
    <div key={key} style={style}>
      <MemoizedItemCard 
        item={filteredData[index]}
        onUpdate={handleUpdate}
      />
    </div>
  ), [filteredData, handleUpdate]);
  
  return (
    <AutoSizer>
      {({ height, width }) => (
        <FixedSizeList
          height={height}
          width={width}
          itemCount={filteredData.length}
          itemSize={120}
          itemData={filteredData}
        >
          {rowRenderer}
        </FixedSizeList>
      )}
    </AutoSizer>
  );
};

// Memoized component with intelligent shallow comparison
const MemoizedItemCard = memo(ItemCard, (prevProps, nextProps) => {
  return (
    prevProps.item.id === nextProps.item.id &&
    prevProps.item.updatedAt === nextProps.item.updatedAt
  );
});
```

## Configuration

`.claude/performance-turbo-config.json`:

```json
{
  "budgets": {
    "strict": {
      "bundleSize": "250KB",
      "firstContentfulPaint": "1.5s",
      "largestContentfulPaint": "2.5s",
      "firstInputDelay": "100ms",
      "cumulativeLayoutShift": "0.1",
      "totalBlockingTime": "200ms"
    },
    "moderate": {
      "bundleSize": "500KB",
      "firstContentfulPaint": "2.5s",
      "largestContentfulPaint": "4s",
      "firstInputDelay": "200ms",
      "cumulativeLayoutShift": "0.15",
      "totalBlockingTime": "400ms"
    },
    "relaxed": {
      "bundleSize": "1MB",
      "firstContentfulPaint": "3s",
      "largestContentfulPaint": "5s",
      "firstInputDelay": "300ms",
      "cumulativeLayoutShift": "0.25",
      "totalBlockingTime": "600ms"
    }
  },
  "optimizations": {
    "bundle": {
      "enabled": true,
      "treeshaking": true,
      "codeSplitting": true,
      "dynamicImports": true,
      "minification": true,
      "compression": "gzip",
      "unusedCodeElimination": true
    },
    "runtime": {
      "enabled": true,
      "memoization": true,
      "virtualization": true,
      "lazyLoading": true,
      "asyncComponents": true,
      "renderOptimization": true
    },
    "memory": {
      "enabled": true,
      "leakDetection": true,
      "cacheOptimization": true,
      "garbageCollection": true,
      "objectPooling": false
    },
    "network": {
      "enabled": true,
      "requestBatching": true,
      "caching": true,
      "compression": true,
      "prefetching": true,
      "serviceWorker": true
    },
    "database": {
      "enabled": true,
      "queryOptimization": true,
      "indexSuggestions": true,
      "connectionPooling": true,
      "cachingLayer": true,
      "eagerLoading": true
    }
  },
  "targets": {
    "web": {
      "focus": ["bundle", "runtime", "network"],
      "frameworks": ["react", "vue", "angular"],
      "metrics": ["lcp", "fid", "cls"]
    },
    "mobile": {
      "focus": ["memory", "battery", "network"],
      "constraints": "low-end-devices",
      "metrics": ["tti", "fcp", "memory"]
    },
    "ssr": {
      "focus": ["ttfb", "hydration", "caching"],
      "metrics": ["ttfb", "fcp", "tti"]
    }
  },
  "monitoring": {
    "realtime": true,
    "webVitals": true,
    "customMetrics": true,
    "performanceObserver": true,
    "resourceTiming": true
  }
}
```

## Command Output

### Performance Analysis
```
⚡ CLAUDE POWER - PERFORMANCE TURBO ANALYSIS
===========================================

📊 PERFORMANCE BASELINE:
┌─────────────────────────┬─────────┬─────────┬─────────┐
│ Metric                  │ Actual  │ Target  │ Status  │
├─────────────────────────┼─────────┼─────────┼─────────┤
│ Bundle Size             │ 847KB   │ 250KB   │ ❌ 238% │
│ First Contentful Paint  │ 3.2s    │ 1.5s    │ ❌ 213% │
│ Largest Contentful Paint│ 4.8s    │ 2.5s    │ ❌ 192% │
│ First Input Delay       │ 180ms   │ 100ms   │ ❌ 180% │
│ Cumulative Layout Shift │ 0.23    │ 0.1     │ ❌ 230% │
│ Total Blocking Time     │ 520ms   │ 200ms   │ ❌ 260% │
└─────────────────────────┴─────────┴─────────┴─────────┘

🔍 IDENTIFIED BOTTLENECKS:
• Large JavaScript bundles (40% of the problem)
• Unoptimized images (25% of the problem)
• Excessive re-renders (20% of the problem)  
• Inefficient database queries (10% of the problem)
• Poor caching strategy (5% of the problem)

🎯 OPTIMIZATION OPPORTUNITIES:
• Bundle splitting: -65% bundle size potential
• Image optimization: -40% load time potential
• Code memoization: -50% re-renders potential
• Query optimization: -70% database time potential
• Cache implementation: -80% repeat load time potential
```

### Applied Optimizations
```
⚡ AUTOMATICALLY APPLIED OPTIMIZATIONS:
==========================================

📦 BUNDLE OPTIMIZATION:
✅ Tree-shaking applied to 23 libraries
✅ Code splitting in 15 main routes
✅ Dynamic imports for 8 heavy components
✅ Dead code elimination: 234KB removed
✅ Minification and compression: -45% size

📊 BUNDLE RESULTS:
• Before: 847KB → After: 287KB (-66%)
• Chunks generated: 12 (vs 1 monolithic)
• Initial load time: 3.2s → 1.4s (-56%)

🧠 MEMORY OPTIMIZATION:
✅ Memoization added to 34 components
✅ Virtualization in 6 long lists
✅ Memory leak fixes in 8 components
✅ LRU cache implemented in 12 functions

📊 MEMORY RESULTS:
• Memory usage: -42% average
• GC frequency: -35% collections
• Retained size: -50% improvement

🌐 NETWORK OPTIMIZATION:
✅ Request batching in 15 endpoints
✅ GraphQL added to eliminate over-fetching
✅ Service Worker cache strategy implemented
✅ Image lazy loading in 45 components
✅ Intelligent resource prefetching

📊 NETWORK RESULTS:
• Network requests: -60% reduction
• Cache hit rate: 85% improvement
• Image load time: -70% improvement

🗄️ DATABASE OPTIMIZATION:
✅ 12 queries optimized with eager loading
✅ 8 indexes suggested and implemented
✅ Connection pooling configured
✅ Redis cache layer added

📊 DATABASE RESULTS:
• Query time: -75% average
• Database connections: -50% usage
• Cache hit rate: 92% on frequent queries

📈 FINAL PERFORMANCE:
┌─────────────────────────┬─────────┬─────────┬─────────┐
│ Metric                  │ Before  │ After   │ Improvement │
├─────────────────────────┼─────────┼─────────┼─────────┤
│ Bundle Size             │ 847KB   │ 287KB   │ ✅ -66% │
│ First Contentful Paint  │ 3.2s    │ 1.4s    │ ✅ -56% │
│ Largest Contentful Paint│ 4.8s    │ 2.1s    │ ✅ -56% │
│ First Input Delay       │ 180ms   │ 85ms    │ ✅ -53% │
│ Cumulative Layout Shift │ 0.23    │ 0.08    │ ✅ -65% │
│ Total Blocking Time     │ 520ms   │ 165ms   │ ✅ -68% │
└─────────────────────────┴─────────┴─────────┴─────────┘

🏆 LIGHTHOUSE SCORE:
• Performance: 45 → 94 (+109%)
• Accessibility: 87 → 95 (+9%)
• Best Practices: 78 → 96 (+23%)
• SEO: 92 → 98 (+7%)
• PWA: N/A → 85 (New)

💰 BUSINESS IMPACT:
• Page load speed: +156% improvement
• User engagement: +34% estimated increase
• SEO ranking: +12% potential boost
• Conversion rate: +18% estimated increase
• Server costs: -25% reduction
```

### Monitoring Setup
```
📊 PERFORMANCE MONITORING CONFIGURED:
=====================================

📈 REAL-TIME METRICS:
• Web Vitals tracking enabled
• Custom performance marks added
• User experience monitoring activated
• Error tracking with performance context

🎯 ALERTS CONFIGURED:
• LCP > 2.5s (Critical)
• FID > 100ms (Warning)  
• CLS > 0.1 (Warning)
• Bundle size > 300KB (Warning)
• Memory usage > 100MB (Critical)

📊 DASHBOARDS:
• Performance dashboard in Grafana
• Real-time monitoring in DataDog
• Weekly performance reports
• Automatic regression detection

🔔 NOTIFICATIONS:
• Slack alerts for regressions
• Weekly email reports
• GitHub PR performance comments
• Automated performance budgets
```

## Advanced Integration

### GitHub Actions
```yaml
name: Performance Turbo

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  performance-optimization:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        
      - name: Install dependencies
        run: npm ci
        
      - name: Run performance optimization
        run: |
          npx claude-power performance-turbo \
            --target=web \
            --budget=strict \
            --mode=safe \
            --output=json > performance-results.json
            
      - name: Run Lighthouse CI
        run: |
          npm run build
          npx lhci autorun
          
      - name: Performance Budget Check
        run: |
          BUNDLE_SIZE=$(du -s dist/ | cut -f1)
          if [ $BUNDLE_SIZE -gt 300 ]; then
            echo "❌ Bundle size exceeds budget: ${BUNDLE_SIZE}KB > 300KB"
            exit 1
          fi
          
      - name: Comment PR with results
        uses: actions/github-script@v6
        with:
          script: |\
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('performance-results.json'));
            
            const comment = `
            ## ⚡ Performance Optimization Results
            
            ### 📊 Metrics Improvement:
            | Metric | Before | After | Improvement |
            |--------|--------|-------|-------------|
            | Bundle Size | ${results.before.bundleSize} | ${results.after.bundleSize} | ${results.improvement.bundleSize} |
            | FCP | ${results.before.fcp} | ${results.after.fcp} | ${results.improvement.fcp} |
            | LCP | ${results.before.lcp} | ${results.after.lcp} | ${results.improvement.lcp} |
            
            ### 🎯 Lighthouse Score: ${results.lighthouse.performance}/100
            
            ${results.lighthouse.performance >= 90 ? '✅' : '⚠️'} Performance Score
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

*Part of the **Claude Power** ecosystem - Perfect performance automatically* ⚡🚀 
