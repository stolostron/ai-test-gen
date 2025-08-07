package destroy_cluster

import (
	"context"

	"github.com/onsi/ginkgo/v2"
	"github.com/onsi/gomega"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

var _ = ginkgo.Describe("destroy cluster", ginkgo.Label("destroy"), func() {

	ginkgo.It("RHACM4K-46702: CLC: Destroy an AWS managed cluster via ClusterDeployment", ginkgo.Label("aws"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "cloud=Amazon,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})

	ginkgo.It("RHACM4K-46704: CLC: Destroy an GCP managed cluster via ClusterDeployment", ginkgo.Label("gcp"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "cloud=Google,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})

	ginkgo.It("RHACM4K-46703: CLC: Destroy an Azure managed cluster via ClusterDeployment", ginkgo.Label("azure"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "cloud=Azure,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})
})
