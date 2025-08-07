package machine_pools_test

import (
	"fmt"
	"os"
	"testing"

	"github.com/onsi/ginkgo/v2"

	"github.com/onsi/gomega"

	"github.com/stolostron/acmqe-clc-test/pkg/utils"
	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
	reporter "github.com/stolostron/acmqe-go-library/pkg/reporter"
)

const (
	kubeConfigFileEnv = "KUBECONFIG"
)

var (
	clients  *utils.Clients
	Appliers *libgoclusters.Appliers
)

func TestMachinePools(t *testing.T) {
	gomega.RegisterFailHandler(ginkgo.Fail)
	ginkgo.RunSpecs(t, "MachinePools Suite")
}

var _ = ginkgo.BeforeSuite(func() {
	clients = utils.NewClients(kubeConfigFileEnv)
	RestConfig, _ := utils.NewKubeConfig(kubeConfigFileEnv)
	Appliers = libgoclusters.NewAppliers(RestConfig)
})

var _ = ginkgo.ReportAfterSuite("CLC Machine Pools Report", func(report ginkgo.Report) {
	junitReportFile := os.Getenv("JUNIT_REPORT_FILE")
	if junitReportFile != "" {
		err := reporter.GenerateJUnitReport(report, junitReportFile)
		if err != nil {
			fmt.Printf("Failed to generate the report due to: %v", err)
		}
	}
})
