package docker

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestParseHTTPLogLine(t *testing.T) {
	logLine := "172.69.214.214 - - [17/Dec/2024:03:14:51 +0000] \"GET /api/legacy/celery/task/c139737b-2661-4c0a-b745-11d4db84d0df/ HTTP/1.1\" 200 149 \"https://synth.fourthievesvinegar.org/network?tab=IPP&target=Clc1cc2c(cc1)N(C(%3DO)N2)C5CCN(CCCN4c3ccccc3NC4%3DO)CC5\" \"Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0\""

	parsed, err := parseHTTPLogLine(logLine)
	if err != nil {
		t.Fatalf("error parsing log line: %v", err)
	}

	assert.Equal(t, parsed.SourceIP, "172.69.214.214")
	assert.Equal(t, parsed.Method, "GET")
	assert.Equal(t, parsed.Status, 200)
	assert.Equal(t, parsed.Timestamp.Day(), 17)
}
