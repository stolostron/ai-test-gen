package import_cluster

import (
	"context"
	"fmt"
	"os"
	"testing"

	"github.com/onsi/ginkgo/v2"
	"github.com/onsi/gomega"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/klog"

	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
	reporter "github.com/stolostron/acmqe-go-library/pkg/reporter"

	"github.com/stolostron/acmqe-clc-test/pkg/utils"
)

const (
	eventuallyTimeout  = 600
	eventuallyInterval = 10
	kubeConfigFileEnv  = "KUBECONFIG"
)

func init() {
	klog.SetOutput(ginkgo.GinkgoWriter)
	klog.InitFlags(nil)
}

func TestImport(t *testing.T) {
	gomega.RegisterFailHandler(ginkgo.Fail)
	ginkgo.RunSpecs(t, "CLC Import Cluster suite")
}

var (
	mceTargetNameSpace string
	Appliers           *libgoclusters.Appliers
)

// This suite is sensitive to the following environment variables:
// KUBECONFIG is the location of the kubeconfig file to be used
var _ = ginkgo.BeforeSuite(func() {
	RestConfig, _ := utils.NewKubeConfig(kubeConfigFileEnv)
	Appliers = libgoclusters.NewAppliers(RestConfig)

	gvr := schema.GroupVersionResource{
		Group:    "multicluster.openshift.io",
		Version:  "v1",
		Resource: "multiclusterengines",
	}
	mceList, err := Appliers.ApplierBuilder.GetDynamicClient().Resource(gvr).List(context.TODO(), metav1.ListOptions{})
	gomega.Expect(err).ToNot(gomega.HaveOccurred())
	for _, mce := range mceList.Items {
		if _, ok := mce.Object["spec"]; ok {
			mceTargetNameSpace = mce.Object["spec"].(map[string]interface{})["targetNamespace"].(string)
		}
	}
})

var _ = ginkgo.ReportAfterSuite("CLC Import Cluster Report", func(report ginkgo.Report) {
	junitReportFile := os.Getenv("JUNIT_REPORT_FILE")
	if junitReportFile != "" {
		err := reporter.GenerateJUnitReport(report, junitReportFile)
		if err != nil {
			fmt.Printf("Failed to generate the report due to: %v", err)
		}
	}
})
