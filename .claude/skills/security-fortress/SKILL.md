---
name: security-fortress
description: "Security scanning and automatic vulnerability protection"
---

# Security Fortress Command

Automatic and proactive threat protection using advanced AI to create an impenetrable security fortress.

## Description

The `/security-fortress` command establishes a complete security shield around your application:

- **Real-time vulnerability analysis**
- **Automatic protection** against common attacks
- **Automatic configuration hardening**
- **Proactive threat monitoring**
- **Automatic compliance** with security standards
- **Automated incident response**
- **Automatically applied security patches**
- **Continuous penetration testing**
- **Complete and automatic audit trails**

## Usage

```
/security-fortress [directory] [--scan] [--harden] [--monitor] [--compliance]
```

### Parameters

- `directory`: specific directory to secure
- `--scan`: Scan types (static, dynamic, dependency, secrets, compliance)
- `--harden`: Hardening level (basic, advanced, paranoid)
- `--monitor`: Real-time monitoring (threats, intrusion, anomaly)
- `--compliance`: Compliance standards (owasp, sox, gdpr, hipaa, pci)
- `--auto-fix`: Apply fixes automatically
- `--penetration-test`: Execute penetration testing
- `--audit-trail`: Generate complete audit trail

### Examples

```
/security-fortress
/security-fortress src/ --scan=static,dependency --harden=advanced
/security-fortress --compliance=gdpr,sox --auto-fix --audit-trail
/security-fortress backend/ --monitor=threats,intrusion --harden=paranoid
/security-fortress --penetration-test --scan=dynamic
/security-fortress api/ --compliance=pci --monitor=anomaly
```

## Automatic Protections

### 🛡️ Input Validation & Sanitization
```javascript
// ❌ BEFORE - Vulnerable to attacks
const UserController = {
  async createUser(req, res) {
    const { name, email, bio } = req.body;
    
    // SQL Injection vulnerable
    const query = `INSERT INTO users (name, email, bio) VALUES ('${name}', '${email}', '${bio}')`;
    await db.query(query);
    
    // XSS vulnerable - direct render
    res.json({ message: `User ${name} created successfully!` });
  },
  
  async updateProfile(req, res) {
    const userId = req.params.id; // No validation
    const data = req.body; // No sanitization
    
    await User.update(data, { where: { id: userId } });
    res.json({ success: true });
  }
};

// ✅ AFTER - Automatically Protected
import { body, param, validationResult } from 'express-validator';
import DOMPurify from 'dompurify';
import rateLimit from 'express-rate-limit';

const UserController = {
  // Automatically added Rate limiting
  createUserLimiter: rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 requests per window
    message: 'Too many user creation attempts'
  }),
  
  // Automatically added Validation middleware
  validateCreateUser: [
    body('name')
      .isLength({ min: 2, max: 50 })
      .matches(/^[a-zA-Z\s]+$/)
      .withMessage('Name must contain only letters and spaces'),
    body('email')
      .isEmail()
      .normalizeEmail()
      .withMessage('Valid email required'),
    body('bio')
      .optional()
      .isLength({ max: 500 })
      .withMessage('Bio must be less than 500 characters')
  ],
  
  async createUser(req, res) {
    // Input validation check
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ 
        errors: errors.array(),
        timestamp: new Date().toISOString(),
        requestId: req.id
      });
    }
    
    const { name, email, bio } = req.body;
    
    // Automatically added Sanitization
    const sanitizedData = {
      name: DOMPurify.sanitize(name.trim()),
      email: email.toLowerCase().trim(),
      bio: bio ? DOMPurify.sanitize(bio.trim()) : null
    };
    
    try {
      // Automatically applied Prepared statements
      const user = await User.create(sanitizedData);
      
      // Automatically added Audit log
      await AuditLog.create({
        action: 'USER_CREATED',
        userId: user.id,
        metadata: { email: sanitizedData.email },
        ipAddress: req.ip,
        userAgent: req.get('User-Agent'),
        timestamp: new Date()
      });
      
      // Response sanitization
      res.json({ 
        message: 'User created successfully',
        userId: user.id,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      // Error logging without sensitive information
      logger.error('User creation failed', {
        error: error.message,
        requestId: req.id,
        timestamp: new Date().toISOString()
      });
      
      res.status(500).json({ 
        message: 'Internal server error',
        requestId: req.id
      });
    }
  }
};
```

### 🔐 Authentication & Authorization
```javascript
// ❌ BEFORE - Weak Authentication
const auth = {
  async login(req, res) {
    const { email, password } = req.body;
    const user = await User.findOne({ where: { email } });
    
    // Vulnerable password comparison
    if (user && user.password === password) {
      const token = jwt.sign({ userId: user.id }, 'secret-key');
      res.json({ token });
    } else {
      res.status(401).json({ message: 'Invalid credentials' });
    }
  },
  
  authenticate(req, res, next) {
    const token = req.headers.authorization;
    const decoded = jwt.verify(token, 'secret-key');
    req.user = decoded;
    next();
  }
};

// ✅ AFTER - Automatically Reinforced Authentication
import bcrypt from 'bcrypt';
import speakeasy from 'speakeasy';
import { RateLimiterRedis } from 'rate-limiter-flexible';

const auth = {
  // Brute force protection
  bruteForceProtection: new RateLimiterRedis({
    storeClient: redisClient,
    keyPrefix: 'login_fail',
    points: 5, // Number of attempts
    duration: 900, // Per 15 minutes
    blockDuration: 900 // Block for 15 minutes
  }),
  
  async login(req, res) {
    const { email, password, totpCode } = req.body;
    const clientIp = req.ip;
    
    try {
      // Check brute force protection
      await this.bruteForceProtection.consume(clientIp);
      
      // Enhanced user lookup with timing attack protection
      const user = await User.findOne({ 
        where: { email: email.toLowerCase() },
        attributes: ['id', 'email', 'passwordHash', 'totpSecret', 'isActive', 'lockoutUntil']
      });
      
      // Account lockout check
      if (user?.lockoutUntil && user.lockoutUntil > new Date()) {
        return res.status(423).json({ 
          message: 'Account temporarily locked',
          lockoutUntil: user.lockoutUntil
        });
      }
      
      // Constant-time password verification
      const isValidPassword = user ? 
        await bcrypt.compare(password, user.passwordHash) : 
        await bcrypt.compare(password, '$2b$12$dummy.hash.to.prevent.timing.attacks');
      
      if (!user || !isValidPassword || !user.isActive) {
        // Consistent response time for security
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Log failed attempt
        await SecurityLog.create({
          event: 'LOGIN_FAILED',
          email,
          ipAddress: clientIp,
          userAgent: req.get('User-Agent'),
          timestamp: new Date()
        });
        
        return res.status(401).json({ 
          message: 'Invalid credentials',
          timestamp: new Date().toISOString()
        });
      }
      
      // TOTP verification (if enabled)
      if (user.totpSecret) {
        if (!totpCode) {
          return res.status(401).json({ 
            message: 'TOTP code required',
            requireTOTP: true
          });
        }
        
        const verified = speakeasy.totp.verify({
          secret: user.totpSecret,
          encoding: 'base32',
          token: totpCode,
          window: 2
        });
        
        if (!verified) {
          return res.status(401).json({ message: 'Invalid TOTP code' });
        }
      }
      
      // Generate secure session
      const sessionId = crypto.randomUUID();
      const tokenPayload = {
        userId: user.id,
        sessionId,
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
      };
      
      const token = jwt.sign(tokenPayload, process.env.JWT_SECRET, {
        algorithm: 'HS256'
      });
      
      // Store session in Redis
      await redisClient.setex(
        `session:${sessionId}`,
        24 * 60 * 60,
        JSON.stringify({
          userId: user.id,
          ipAddress: clientIp,
          userAgent: req.get('User-Agent'),
          createdAt: new Date()
        })
      );
      
      // Success audit log
      await SecurityLog.create({
        event: 'LOGIN_SUCCESS',
        userId: user.id,
        sessionId,
        ipAddress: clientIp,
        userAgent: req.get('User-Agent'),
        timestamp: new Date()
      });
      
      // Reset brute force counter on successful login
      await this.bruteForceProtection.delete(clientIp);
      
      res.json({ 
        token,
        expiresIn: 24 * 60 * 60 * 1000,
        requirePasswordChange: user.requirePasswordChange || false
      });
      
    } catch (error) {
      if (error.remainingHits !== undefined) {
        return res.status(429).json({
          message: 'Too many login attempts',
          retryAfter: error.msBeforeNext
        });
      }
      
      logger.error('Login error', { error: error.message, email });
      res.status(500).json({ message: 'Internal server error' });
    }
  }
};
```

### 🔒 Data Protection & Encryption
```javascript
// ❌ BEFORE - Unprotected Data
const UserService = {
  async createUser(userData) {
    // Sensitive data unencrypted
    const user = await User.create({
      email: userData.email,
      ssn: userData.ssn,
      creditCard: userData.creditCard,
      address: userData.address
    });
    
    return user;
  },
  
  async getUser(id) {
    return await User.findById(id);
  }
};

// ✅ AFTER - Automatic Data Protection
import crypto from 'crypto';
import { encrypt, decrypt } from '../utils/encryption';

const UserService = {
  // Automatically added Field-level encryption
  encryptionConfig: {
    ssn: { encrypt: true, algorithm: 'aes-256-gcm' },
    creditCard: { encrypt: true, algorithm: 'aes-256-gcm' },
    address: { encrypt: true, algorithm: 'aes-256-gcm' },
    email: { hash: true, algorithm: 'sha-256' } // For searches
  },
  
  async createUser(userData) {
    // Automatic Data classification
    const classifiedData = await this.classifyData(userData);
    
    // Automatic Encryption of sensitive fields
    const encryptedData = {};
    
    for (const [field, value] of Object.entries(userData)) {
      const config = this.encryptionConfig[field];
      
      if (config?.encrypt) {
        encryptedData[field] = await encrypt(value, config.algorithm);
        // Hash for indexing
        encryptedData[`${field}_hash`] = crypto
          .createHash('sha-256')
          .update(value)
          .digest('hex');
      } else if (config?.hash) {
        encryptedData[field] = value; // Store original for auth
        encryptedData[`${field}_hash`] = crypto
          .createHash('sha-256')
          .update(value)
          .digest('hex');
      } else {
        encryptedData[field] = value;
      }
    }
    
    const user = await User.create(encryptedData);
    
    // Audit log for sensitive data
    await DataAccessLog.create({
      action: 'USER_CREATED',
      userId: user.id,
      dataTypes: Object.keys(classifiedData.sensitive),
      ipAddress: req.ip,
      timestamp: new Date()
    });
    
    return this.sanitizeForResponse(user);
  },
  
  async getUser(id, requesterUserId) {
    // Access control check
    const hasAccess = await this.checkDataAccess(requesterUserId, id);
    if (!hasAccess) {
      throw new Error('Insufficient permissions');
    }
    
    const user = await User.findById(id);
    if (!user) return null;
    
    // Automatic decryption for authorized fields
    const decryptedUser = {};
    
    for (const [field, value] of Object.entries(user.toJSON())) {
      const config = this.encryptionConfig[field];
      
      if (config?.encrypt && value) {
        // Check if the user has permissions for this field
        const hasFieldAccess = await this.checkFieldAccess(
          requesterUserId, 
          field, 
          id
        );
        
        if (hasFieldAccess) {
          decryptedUser[field] = await decrypt(value, config.algorithm);
        } else {
          decryptedUser[field] = '[REDACTED]';
        }
      } else if (!field.endsWith('_hash')) {
        decryptedUser[field] = value;
      }
    }
    
    // Audit log for data access
    await DataAccessLog.create({
      action: 'USER_ACCESSED',
      userId: id,
      accessedBy: requesterUserId,
      fieldsAccessed: Object.keys(decryptedUser),
      timestamp: new Date()
    });
    
    return this.sanitizeForResponse(decryptedUser);
  },
  
  // Data Loss Prevention
  sanitizeForResponse(userData) {
    const sanitized = { ...userData };
    
    // Remove internal fields
    delete sanitized.passwordHash;
    delete sanitized.totpSecret;
    
    // Mask sensitive fields if not fully authorized
    if (sanitized.ssn && !this.isFullyAuthorized()) {
      sanitized.ssn = `***-**-${sanitized.ssn.slice(-4)}`;
    }
    
    if (sanitized.creditCard && !this.isFullyAuthorized()) {
      sanitized.creditCard = `****-****-****-${sanitized.creditCard.slice(-4)}`;
    }
    
    return sanitized;
  }
};
```

### 🚨 Threat Detection & Response
```javascript
// Automatic threat detection system
const ThreatDetection = {
  // Anomaly detection with machine learning
  async detectAnomalies(req, res, next) {
    const userBehavior = {
      ipAddress: req.ip,
      userAgent: req.get('User-Agent'),
      timestamp: new Date(),
      endpoint: req.path,
      method: req.method,
      userId: req.user?.id
    };
    
    // Automatically detected anomalous patterns
    const anomalies = [];
    
    // Geographic anomaly
    const userLocation = await this.getLocationFromIP(req.ip);
    const recentLocations = await this.getRecentUserLocations(req.user?.id);
    
    if (this.isGeographicAnomaly(userLocation, recentLocations)) {
      anomalies.push({
        type: 'GEOGRAPHIC_ANOMALY',
        risk: 'HIGH',
        details: `Login from unusual location: ${userLocation.country}`
      });
    }
    
    // Time-based anomaly
    const currentHour = new Date().getHours();
    const typicalHours = await this.getUserTypicalHours(req.user?.id);
    
    if (!typicalHours.includes(currentHour)) {
      anomalies.push({
        type: 'TEMPORAL_ANOMALY',
        risk: 'MEDIUM',
        details: `Login at unusual time: ${currentHour}:00`
      });
    }
    
    // Behavioral anomaly
    const recentRequests = await this.getRecentRequests(req.user?.id);
    const isUnusualPattern = await this.detectUnusualPattern(recentRequests);
    
    if (isUnusualPattern) {
      anomalies.push({
        type: 'BEHAVIORAL_ANOMALY',
        risk: 'HIGH',
        details: 'Unusual request pattern detected'
      });
    }
    
    // Automatic threat response
    if (anomalies.some(a => a.risk === 'HIGH')) {
      // Step-up authentication
      req.requireStepUp = true;
      
      // Alert security team
      await this.alertSecurityTeam({
        userId: req.user?.id,
        anomalies,
        request: userBehavior
      });
      
      // Stricter rate limit
      await this.applyStrictRateLimit(req.ip);
    }
    
    // Log all anomalies
    if (anomalies.length > 0) {
      await ThreatLog.create({
        userId: req.user?.id,
        anomalies,
        userBehavior,
        actionTaken: req.requireStepUp ? 'STEP_UP_AUTH' : 'LOGGED'
      });
    }
    
    next();
  },
  
  // Automated incident response
  async respondToIncident(threatLevel, details) {
    switch (threatLevel) {
      case 'CRITICAL':
        // Immediate lockdown
        await this.lockdownUser(details.userId);
        await this.notifySOC(details);
        await this.createIncidentTicket(details);
        break;
        
      case 'HIGH':
        // Enhanced monitoring
        await this.enableEnhancedMonitoring(details.userId);
        await this.requireAdditionalAuth(details.userId);
        await this.notifySecurityTeam(details);
        break;
        
      case 'MEDIUM':
        // Log and monitor
        await this.increaseMonitoring(details.userId);
        await this.logSecurityEvent(details);
        break;
    }
  }
};
```

## Configuration

`.claude/security-fortress-config.json`:

```json
{
  "scanning": {
    "static": {
      "enabled": true,
      "tools": ["semgrep", "codeql", "sonarqube"],
      "rules": ["owasp-top10", "cwe-top25"],
      "severity": ["high", "critical"]
    },
    "dynamic": {
      "enabled": true,
      "tools": ["zap", "burp"],
      "endpoints": "auto-discover",
      "authentication": "auto-configure"
    },
    "dependency": {
      "enabled": true,
      "tools": ["snyk", "npm-audit", "github-advisory"],
      "autoUpdate": "security-only",
      "allowedLicenses": ["MIT", "Apache-2.0", "BSD"]
    },
    "secrets": {
      "enabled": true,
      "tools": ["trufflesecurity", "detect-secrets"],
      "patterns": ["api-keys", "passwords", "certificates"],
      "excludePaths": ["test/", "docs/"]
    }
  },
  "hardening": {
    "headers": {
      "contentSecurityPolicy": "strict",
      "strictTransportSecurity": true,
      "xFrameOptions": "DENY",
      "xContentTypeOptions": true,
      "referrerPolicy": "strict-origin-when-cross-origin"
    },
    "authentication": {
      "passwordPolicy": {
        "minLength": 12,
        "requireSpecialChars": true,
        "requireNumbers": true,
        "preventReuse": 12
      },
      "mfa": {
        "enforce": true,
        "methods": ["totp", "sms", "email"],
        "backupCodes": true
      },
      "session": {
        "timeout": 3600,
        "absoluteTimeout": 28800,
        "renewOnActivity": true
      }
    },
    "rateLimit": {
      "global": "1000 req/hour",
      "perUser": "100 req/min",
      "perIP": "60 req/min",
      "sensitive": "5 req/min"
    }
  },
  "monitoring": {
    "realtime": {
      "enabled": true,
      "events": ["login", "data-access", "privilege-escalation"],
      "anomalyDetection": true,
      "machLearning": true
    },
    "alerts": {
      "channels": ["slack", "email", "pagerduty"],
      "severity": {
        "critical": "immediate",
        "high": "5min",
        "medium": "1hour"
      }
    },
    "siem": {
      "enabled": true,
      "provider": "splunk",
      "retention": "1year"
    }
  },
  "compliance": {
    "standards": {
      "owasp": {
        "enabled": true,
        "version": "2021",
        "categories": "all"
      },
      "sox": {
        "enabled": false,
        "auditTrail": true,
        "dataRetention": "7years"
      },
      "gdpr": {
        "enabled": true,
        "dataMapping": true,
        "consentManagement": true,
        "rightToErasure": true
      },
      "hipaa": {
        "enabled": false,
        "encryption": "aes-256",
        "accessControls": "rbac"
      }
    }
  }
}
```

## Command Output

### Security Assessment
```
🛡️ CLAUDE POWER - SECURITY FORTRESS ANALYSIS
============================================

🔍 SECURITY ASSESSMENT COMPLETED:
scanned files: 1,247
detected vulnerabilities: 23
analysis time: 3m 42s

🚨 VULNERABILITIES BY SEVERITY:
┌─────────────────────┬─────────┬─────────────┬─────────────┐
│ Severity            │ Count   │ Fixed       │ Remaining   │
├─────────────────────┼─────────┼─────────────┼─────────────┤
│ Critical            │    3    │     3       │     0       │
│ High                │    8    │     7       │     1       │
│ Medium              │   12    │    10       │     2       │
│ Low                 │    0    │     0       │     0       │
└─────────────────────┴─────────┴─────────────┴─────────────┘

🎯 OWASP TOP 10 COMPLIANCE:
✅ A01: Broken Access Control - Compliant
✅ A02: Cryptographic Failures - Compliant  
✅ A03: Injection - Compliant
⚠️ A04: Insecure Design - 1 issue remaining
✅ A05: Security Misconfiguration - Compliant
✅ A06: Vulnerable Components - Compliant
✅ A07: Identity/Auth Failures - Compliant
✅ A08: Software/Data Integrity - Compliant
✅ A09: Security Logging/Monitoring - Compliant
✅ A10: Server-Side Request Forgery - Compliant

📊 SECURITY SCORE: 96/100 (Excellent)
```

### Protections Activated
```
🛡️ AUTOMATICALLY ACTIVATED PROTECTIONS:
==========================================

🔐 AUTHENTICATION & AUTHORIZATION:
✅ Multi-factor authentication enforced
✅ Password policy strengthened (12+ chars, complexity)
✅ Session management hardened (timeout, rotation)
✅ Brute force protection activated
✅ Account lockout policies implemented

🛡️ INPUT VALIDATION & SANITIZATION:
✅ XSS protection on 45 input fields
✅ SQL injection prevention on 23 queries
✅ CSRF tokens implemented on all forms
✅ File upload validation enhanced
✅ Input rate limiting applied

🔒 DATA PROTECTION:
✅ Field-level encryption on sensitive data
✅ Data classification system implemented
✅ Access logging for all sensitive operations
✅ Data masking in logs and responses
✅ Backup encryption enabled

🌐 NETWORK SECURITY:
✅ Security headers configured (CSP, HSTS, etc.)
✅ TLS 1.3 enforced with perfect forward secrecy
✅ API rate limiting implemented
✅ CORS policies hardened
✅ Request/response size limits set

🚨 THREAT DETECTION:
✅ Real-time anomaly detection active
✅ Geographic anomaly alerts configured
✅ Behavioral pattern monitoring enabled
✅ Failed login attempt tracking
✅ Privilege escalation monitoring

📊 COMPLIANCE STATUS:
✅ OWASP Top 10 - 100% compliant
✅ GDPR - Data protection ready
⚠️ SOX - Audit trail enhancement needed
✅ Security best practices - Implemented

🔔 MONITORING & ALERTING:
✅ Security incident dashboard configured
✅ Slack alerts for critical events
✅ Weekly security reports scheduled
✅ Penetration test automation setup
✅ Vulnerability scanning scheduled daily
```

### Incident Response Plan
```
🚨 AUTOMATED INCIDENT RESPONSE ACTIVATED:
========================================

📋 RESPONSE PROCEDURES:
• Critical: Immediate lockdown + SOC notification
• High: Enhanced monitoring + step-up auth
• Medium: Increased logging + team alert
• Low: Standard logging + weekly review

🎯 AUTOMATED ACTIONS:
✅ User lockdown procedures defined
✅ Incident escalation workflows active
✅ Forensic data collection automated
✅ Communication templates prepared
✅ Recovery procedures documented

📞 CONTACT CHAIN:
• Security Team: security@company.com
• SOC: +1-555-0199 (24/7)
• Legal: legal@company.com
• Executive: exec@company.com

⏱️ RESPONSE TIMES:
• Detection: < 5 minutes
• Assessment: < 15 minutes  
• Containment: < 30 minutes
• Communication: < 1 hour
• Recovery: < 4 hours
```

---

*Part of the **Claude Power** ecosystem - Automatic impenetrable security* 🛡️🚀 
