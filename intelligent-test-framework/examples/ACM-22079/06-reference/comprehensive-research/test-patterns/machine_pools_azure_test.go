package machine_pools

import (
	"fmt"

	"github.com/onsi/ginkgo/v2"
	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("Azure Machine Pools", ginkgo.Label("machinepools"), func() {
	ginkgo.BeforeEach(func() {
		var cloudProvider = "azure"
		_, err := libgoclusters.GetHiveClusterNamespaces(Appliers, cloudProvider)
		if err != nil {
			ginkgo.Skip(fmt.Sprintf("Skipping test due to failure in GetHiveClusterNamespaces: %v", err))
		}
	})

	// Scale Up
	ginkgo.It("RHACM4K-24026 - As a cluster-admin with an ACM-created Azure cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24026", "scale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", false, 1, 0, 0, "", "")
	})

	// Scale Down
	ginkgo.It("RHACM4K-24032 - As a cluster-admin with an ACM-created Azure cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24032", "scale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", false, -1, 0, 0, "", "")
	})

	// Autoscale Up
	ginkgo.It("RHACM4K-24039 - As a cluster-admin with an ACM-created Azure cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24039", "autoscale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", true, 0, 1, 1, "", "")
	})

	// Autoscale Down
	ginkgo.It("RHACM4K-24044 - As a cluster-admin with an ACM-created Azure cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24044", "autoscale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", true, 0, -1, -1, "", "")
	})
})
