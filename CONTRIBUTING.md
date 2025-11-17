# 🤝 Contributing to BHIV HR Platform

**Welcome Contributors!** Thank you for your interest in contributing to the BHIV HR Platform. This guide will help you get started with contributing to our enterprise AI-powered recruiting platform.

---

## 🚀 Quick Start for Contributors

### **Getting Started**
1. **Fork the Repository**: Create your own fork of the project
2. **Clone Locally**: `git clone https://github.com/YOUR_USERNAME/BHIV-HR-Platform.git`
3. **Setup Environment**: Follow our [Quick Start Guide](docs/QUICK_START_GUIDE.md)
4. **Create Branch**: `git checkout -b feature/your-feature-name`
5. **Make Changes**: Implement your improvements
6. **Test Thoroughly**: Run our comprehensive test suite
7. **Submit PR**: Create a pull request with detailed description

### **Development Environment**
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/BHIV-HR-Platform.git
cd BHIV-HR-Platform
cp .env.example .env

# Start development environment
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Verify all services are running
curl http://localhost:8000/health  # Gateway
curl http://localhost:9000/health  # Agent
curl http://localhost:9001/health  # LangGraph
```

---

## 📋 Contribution Guidelines

### **Types of Contributions**
- 🐛 **Bug Fixes**: Fix issues in existing functionality
- ✨ **New Features**: Add new capabilities to the platform
- 📚 **Documentation**: Improve or add documentation
- 🧪 **Testing**: Add or improve test coverage
- 🔒 **Security**: Enhance security features
- ⚡ **Performance**: Optimize system performance
- 🎨 **UI/UX**: Improve user interface and experience

### **Before You Start**
1. **Check Existing Issues**: Look for related issues or feature requests
2. **Create Issue**: If none exists, create a detailed issue first
3. **Discuss Approach**: Comment on the issue to discuss your approach
4. **Get Approval**: Wait for maintainer approval before starting work
5. **Follow Standards**: Adhere to our coding standards and architecture

---

## 🏗️ Development Standards

### **Code Quality Requirements**
```python
# Code Style
- Follow PEP 8 for Python code
- Use type hints for all functions
- Write comprehensive docstrings
- Maintain consistent naming conventions
- Keep functions focused and small

# Example:
def calculate_match_score(
    candidate_skills: List[str], 
    job_requirements: List[str]
) -> float:
    """
    Calculate matching score between candidate skills and job requirements.
    
    Args:
        candidate_skills: List of candidate's skills
        job_requirements: List of job requirements
        
    Returns:
        float: Matching score between 0.0 and 1.0
    """
    # Implementation here
    pass
```

### **Architecture Principles**
- **Microservices**: Maintain service separation
- **API-First**: Design APIs before implementation
- **Security-First**: Security considerations in all changes
- **Performance**: Consider performance impact
- **Scalability**: Design for growth
- **Documentation**: Document all changes

### **Testing Requirements**
```python
# Test Coverage Requirements
- Unit Tests: >90% coverage for new code
- Integration Tests: Test service interactions
- Security Tests: Test security features
- Performance Tests: Verify performance requirements
- End-to-End Tests: Test complete workflows

# Test Structure
tests/
├── unit/           # Unit tests by service
├── integration/    # Service integration tests
├── security/       # Security-specific tests
├── performance/    # Performance benchmarks
└── e2e/           # End-to-end workflow tests
```

---

## 🔧 Development Workflow

### **Branch Strategy**
```bash
# Branch Naming Convention
feature/description-of-feature    # New features
bugfix/description-of-bug        # Bug fixes
security/description-of-fix      # Security improvements
docs/description-of-update       # Documentation updates
test/description-of-tests        # Test improvements

# Examples:
git checkout -b feature/ai-matching-improvements
git checkout -b bugfix/authentication-timeout
git checkout -b security/rate-limiting-enhancement
```

### **Commit Message Format**
```bash
# Commit Message Structure
type(scope): brief description

Detailed explanation of changes made and why.

Fixes #issue_number

# Types:
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Code style changes
refactor: Code refactoring
test:     Test additions/changes
security: Security improvements
perf:     Performance improvements

# Examples:
feat(ai): implement Phase 4 semantic matching algorithm

Add advanced semantic matching using transformer models
for improved candidate-job matching accuracy.

- Implement sentence transformer integration
- Add batch processing for performance
- Include fallback to Phase 3 matching
- Add comprehensive test coverage

Fixes #123
```

### **Pull Request Process**
1. **Create Detailed PR**:
   - Clear title and description
   - Link to related issues
   - List all changes made
   - Include testing information

2. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes made.

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Security improvement
   - [ ] Performance optimization

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests pass
   - [ ] Security tests pass
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] Tests added for new functionality
   - [ ] All tests pass

   ## Related Issues
   Fixes #issue_number
   ```

3. **Review Process**:
   - Automated tests must pass
   - Code review by maintainers
   - Security review for security changes
   - Performance review for performance changes

---

## 🧪 Testing Guidelines

### **Test Requirements**
```python
# Test File Structure
tests/
├── test_gateway.py         # Gateway service tests
├── test_agent.py          # AI agent service tests
├── test_langgraph.py      # LangGraph workflow tests
├── test_security.py       # Security feature tests
├── test_database.py       # Database operation tests
└── test_integration.py    # Cross-service tests

# Test Naming Convention
def test_function_name_expected_behavior():
    """Test that function_name behaves as expected under specific conditions."""
    # Arrange
    # Act
    # Assert
```

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/unit/ -v           # Unit tests
python -m pytest tests/integration/ -v    # Integration tests
python -m pytest tests/security/ -v       # Security tests

# Run with coverage
python -m pytest tests/ --cov=services/ --cov-report=html

# Performance tests
python -m pytest tests/performance/ -v --benchmark-only
```

### **Test Data Management**
```python
# Use fixtures for test data
@pytest.fixture
def sample_candidate():
    return {
        "name": "Test Candidate",
        "email": "test@example.com",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "experience": 3
    }

# Clean up after tests
@pytest.fixture(autouse=True)
def cleanup_database():
    yield
    # Cleanup code here
```

---

## 🔒 Security Considerations

### **Security Review Requirements**
- **Authentication Changes**: Require security team review
- **Authorization Logic**: Test with different user roles
- **Input Validation**: Comprehensive sanitization testing
- **Data Access**: Verify proper access controls
- **API Changes**: Security impact assessment

### **Security Testing**
```python
# Security Test Examples
def test_api_key_validation():
    """Test that invalid API keys are rejected."""
    response = client.get("/v1/candidates", headers={"Authorization": "Bearer invalid_key"})
    assert response.status_code == 401

def test_sql_injection_protection():
    """Test that SQL injection attempts are blocked."""
    malicious_input = "'; DROP TABLE candidates; --"
    response = client.post("/v1/candidates/search", json={"query": malicious_input})
    assert response.status_code == 400  # Bad request due to validation
```

### **Security Checklist**
- [ ] Input validation implemented
- [ ] Authentication tested
- [ ] Authorization verified
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Rate limiting tested
- [ ] Audit logging added

---

## 📚 Documentation Standards

### **Documentation Requirements**
- **Code Documentation**: Comprehensive docstrings
- **API Documentation**: OpenAPI/Swagger specs
- **User Documentation**: Clear user guides
- **Technical Documentation**: Architecture and design docs
- **Change Documentation**: Update relevant docs with changes

### **Documentation Format**
```python
# Function Documentation
def process_candidate_application(
    candidate_id: int, 
    job_id: int, 
    application_data: Dict[str, Any]
) -> ApplicationResult:
    """
    Process a candidate's job application through the AI matching system.
    
    This function handles the complete application workflow including:
    - Candidate profile validation
    - Job requirement matching
    - AI-powered scoring
    - Workflow trigger for notifications
    
    Args:
        candidate_id: Unique identifier for the candidate
        job_id: Unique identifier for the job posting
        application_data: Additional application information
        
    Returns:
        ApplicationResult: Contains match score, status, and next steps
        
    Raises:
        ValidationError: If candidate or job data is invalid
        DatabaseError: If database operations fail
        AIProcessingError: If AI matching fails
        
    Example:
        >>> result = process_candidate_application(123, 456, {"cover_letter": "..."})
        >>> print(f"Match score: {result.match_score}")
        Match score: 0.85
    """
```

---

## 🚀 Feature Development

### **New Feature Process**
1. **Feature Proposal**:
   - Create detailed issue with feature description
   - Include use cases and requirements
   - Discuss implementation approach
   - Get approval from maintainers

2. **Design Phase**:
   - Create technical design document
   - Define API contracts
   - Plan database changes
   - Consider security implications

3. **Implementation**:
   - Follow coding standards
   - Implement comprehensive tests
   - Update documentation
   - Consider backward compatibility

4. **Review & Deployment**:
   - Code review process
   - Security review if needed
   - Performance testing
   - Staged deployment

### **Feature Categories**
```python
# AI/ML Features
- Matching algorithm improvements
- New AI models integration
- Performance optimizations
- Batch processing enhancements

# Security Features
- Authentication enhancements
- Authorization improvements
- Security monitoring
- Compliance features

# User Experience
- Portal improvements
- API enhancements
- Performance optimizations
- Mobile responsiveness

# Infrastructure
- Deployment improvements
- Monitoring enhancements
- Scalability features
- Cost optimizations
```

---

## 🐛 Bug Reporting & Fixing

### **Bug Report Template**
```markdown
## Bug Description
Clear description of the bug and its impact.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- Service: Gateway/Agent/Portal/etc.
- Version: v4.2.0
- Browser: Chrome/Firefox/etc. (if applicable)
- OS: Windows/Mac/Linux

## Additional Context
Screenshots, logs, or other relevant information.
```

### **Bug Fix Process**
1. **Reproduce Bug**: Confirm the issue exists
2. **Root Cause Analysis**: Identify the underlying cause
3. **Fix Implementation**: Implement minimal fix
4. **Test Coverage**: Add tests to prevent regression
5. **Documentation**: Update docs if needed

---

## 📊 Performance Considerations

### **Performance Guidelines**
- **API Response Time**: <100ms for simple endpoints
- **Database Queries**: <50ms for standard queries
- **AI Processing**: <2 seconds for matching
- **Memory Usage**: Monitor and optimize
- **CPU Usage**: Keep under 70% average

### **Performance Testing**
```python
# Performance Test Example
def test_api_response_time():
    """Test that API endpoints respond within acceptable time limits."""
    start_time = time.time()
    response = client.get("/v1/candidates")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 0.1  # 100ms limit
```

---

## 🔄 Deployment & Release

### **Deployment Process**
1. **Development**: Feature branches and testing
2. **Staging**: Integration testing and validation
3. **Production**: Automated deployment via Render
4. **Monitoring**: Post-deployment health checks

### **Release Notes**
```markdown
# Release v4.3.0

## New Features
- Enhanced AI matching algorithm (Phase 4)
- Improved candidate portal UI
- Advanced security monitoring

## Bug Fixes
- Fixed authentication timeout issue
- Resolved database connection pooling
- Corrected rate limiting calculation

## Security Updates
- Updated dependency versions
- Enhanced input validation
- Improved audit logging

## Performance Improvements
- Optimized database queries
- Reduced memory usage
- Faster API response times
```

---

## 📞 Community & Support

### **Communication Channels**
- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code contributions and reviews
- **Documentation**: Comprehensive guides and references

### **Getting Help**
1. **Check Documentation**: Review existing docs first
2. **Search Issues**: Look for similar problems
3. **Create Issue**: Detailed issue with reproduction steps
4. **Community Support**: Engage with other contributors

### **Code of Conduct**
- **Be Respectful**: Treat all contributors with respect
- **Be Collaborative**: Work together towards common goals
- **Be Inclusive**: Welcome contributors from all backgrounds
- **Be Professional**: Maintain professional communication
- **Be Constructive**: Provide helpful feedback and suggestions

---

## 🎯 Contribution Recognition

### **Contributor Levels**
- **First-time Contributors**: Welcome and guidance provided
- **Regular Contributors**: Recognition in release notes
- **Core Contributors**: Elevated permissions and responsibilities
- **Maintainers**: Full project access and decision-making

### **Recognition**
- Contributors listed in release notes
- GitHub contributor statistics
- Special recognition for significant contributions
- Opportunity to become core team member

---

**Thank you for contributing to BHIV HR Platform!** Your contributions help make this enterprise AI-powered recruiting platform better for everyone.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: November 15, 2025 | **Status**: ✅ Complete Guidelines | **Contributors**: Welcome | **Process**: Streamlined | **Support**: Comprehensive