package health

// CheckResult stores the result of a health check.
// Message should contain a human-readable message
// to be displayed to the user.
type CheckResult struct {
	// Success indicates whether the check passed or not.
	Success bool
	// Message contains a human-readable message to be displayed to the user.
	Message string
}
