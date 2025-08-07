package machine_pools

import (
	"fmt"

	"github.com/onsi/ginkgo/v2"
	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("GCP Machine Pools", ginkgo.Label("machinepools"), func() {
	ginkgo.BeforeEach(func() {
		var cloudProvider = "gcp"
		_, err := libgoclusters.GetHiveClusterNamespaces(Appliers, cloudProvider)
		if err != nil {
			ginkgo.Skip(fmt.Sprintf("Skipping test due to failure in GetHiveClusterNamespaces: %v", err))
		}
	})

	// Scale Up
	ginkgo.It("RHACM4K-24025 - As a cluster-admin with an ACM-created GCP cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24025", "scale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", false, 1, 0, 0, "", "")
	})

	// Scale Down
	ginkgo.It("RHACM4K-24031 - As a cluster-admin with an ACM-created GCP cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24031", "scale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", false, -1, 0, 0, "", "")
	})

	// Autoscale Up
	ginkgo.It("RHACM4K-24038 - As a cluster-admin with an ACM-created GCP cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24038", "autoscale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", true, 0, 1, 1, "", "")
	})

	// Autoscale Down
	ginkgo.It("RHACM4K-24043 - As a cluster-admin with an ACM-created GCP cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24043", "autoscale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", true, 0, -1, -1, "", "")
	})
})
